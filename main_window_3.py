import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import Qt, QPoint, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QIcon, QPixmap

from ui.MainWindow_3_UI import Ui_MainWindow

from pages_functions.cpu_and_memory import CPU_and_Memory
from pages_functions.sys_info import System_Information
from pages_functions.os_info import OS_Info
from pages_functions.process_list import Process_List
from pages_functions.file_list import File_List
from pages_functions.terminal import Terminal
from pages_functions.sftp import SFTP
from pages_functions.storage import Storage
from pages_functions.network import SpeedTestApp

from RaspInfo import RaspInfo
from information_string import information_string
import socket
import json

class MyWindow_3(QMainWindow):
    logoutSignal_3 = pyqtSignal()
    def __init__(self):
        super(MyWindow_3, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._starPos = None
        self._endPos = None
        self._tracking = False

        # Get all objects in window
        self.cpu_button = self.ui.cpu_button
        self.sy_info_button = self.ui.sy_info_button
        self.os_info_button = self.ui.os_info_button
        self.process_list_button = self.ui.process_list_button
        self.terminal_button = self.ui.terminal_button
        self.sftp_button = self.ui.sftp_button
        self.storage_button = self.ui.storage_button
        self.network_button = self.ui.network_button
        
        ##Create dict for menu buttons and tab windows
        self.menu_btn_dict = {
            self.cpu_button: CPU_and_Memory,
            self.sy_info_button: System_Information,
            self.os_info_button: OS_Info,
            self.process_list_button: Process_List,
            self.terminal_button: Terminal,
            self.sftp_button: SFTP,
            self.storage_button: Storage,
            self.network_button: SpeedTestApp,
        }

        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)

        #connect signal and slot
        
        self.network_button.clicked.connect(self.show_selected_window)

        self.ui.close_window_btn.clicked.connect(lambda: self.close())
        self.ui.minimize_window_btn.clicked.connect(lambda: self.showMinimized())
        self.ui.restore_window_btn.clicked.connect(lambda: self.restore_or_maximize_window())

        
        #connect signal and send request
        if(self.cpu_button.clicked.connect(lambda:  self.handle_request('get_memory_info'))) :
            if(self.cpu_button.clicked.connect(lambda: self.handle_request('get_temp'))) :
                if(self.cpu_button.clicked.connect(lambda: self.handle_request('get_cpu_percent'))):
                    if(self.cpu_button.clicked.connect(lambda: self.handle_request('cpu_count'))):
                        if(self.cpu_button.clicked.connect(lambda: self.handle_request('cpu_main_core'))):
                            self.cpu_button.clicked.connect(self.show_selected_window)

        if(self.sy_info_button.clicked.connect(lambda: self.handle_request('get_system_info'))):
            if(self.sy_info_button.clicked.connect(lambda: self.handle_request('get_time'))):
                if(self.sy_info_button.clicked.connect(lambda: self.handle_request('get_date'))):
                    self.sy_info_button.clicked.connect(self.show_selected_window)
        
        if(self.os_info_button.clicked.connect(lambda: self.handle_request('get_os_info'))):
            if(self.os_info_button.clicked.connect(lambda: self.handle_request('get_time'))):
                if(self.os_info_button.clicked.connect(lambda: self.handle_request('get_date'))):
                    self.os_info_button.clicked.connect(self.show_selected_window)

        if(self.storage_button.clicked.connect(lambda: self.handle_request('get_disk_usage'))):
            self.storage_button.clicked.connect(self.show_selected_window)
        
        self.process_list_button.clicked.connect(self.show_selected_window)
        
        self.terminal_button.clicked.connect(self.show_selected_window)

        self.sftp_button.clicked.connect(self.show_selected_window)

        self.ui.shutdown_btn.clicked.connect(lambda: self.handle_request('shutdown'))

        self.ui.reboot_btn.clicked.connect(lambda: self.handle_request('reboot'))
        
        #hide the frame and background of the app
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
        else: 
            self.showMaximized()

    def set_btn_checked(self, btn):
        for button in self.menu_btn_dict.keys():
            if button != btn:
                button.setChecked(False)
            else:
                button.setChecked(True)

    def show_selected_window(self):
        # show selected window
        button = self.sender()
        result = self.open_tab_flag(button.text())
        self.set_btn_checked(button)
        if result[0]:
            self.ui.tabWidget.setCurrentIndex(result[1])
        else:
            tab_title = button.text()
            curIndex = self.ui.tabWidget.addTab(self.menu_btn_dict[button](), tab_title)
            self.ui.tabWidget.setCurrentIndex(curIndex)
            self.ui.tabWidget.setVisible(True)

    def open_tab_flag(self, btn_text):
        # check selected window show or not
        open_tab_count = self.ui.tabWidget.count()
        for i in range(open_tab_count):
            tab_title = self.ui.tabWidget.tabText(i)
            if tab_title == btn_text:
                return True, i
            else:
                continue
        return False,

    def close_tab(self, index):
        self.ui.tabWidget.removeTab(index)
        if self.ui.tabWidget.count() == 0:
            self.ui.toolBox.setCurrentIndex(0)

    ## TODO: make the window movable after hide window frame
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if self._tracking:
            self._endPos = a0.pos() - self._starPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self._starPos = QPoint(a0.x(), a0.y())
            self._tracking = True

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self._tracking = False
            self._starPos = None
            self._endPos = None 

    @pyqtSlot()
    def on_disconnect_btn_clicked(self):
        # # Phát tín hiệu để đăng xuất thành công
        self.logoutSignal_3.emit()

    def handle_request(self, data):
        # Gửi yêu cầu đến server và nhận kết quả
        SERVER_HOST = RaspInfo.get_rasp_ip()
        SERVER_PORT = RaspInfo.get_rasp_port()

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        client_socket.send(data.encode())
        response = client_socket.recv(524288).decode('utf-8')

        if data == 'get_memory_info':
            # response = "Total RAM: 921.96484375 MB, Available RAM: 642.81640625 MB, Used RAM: 215.421875 MB Total Swap: 99.99609375 MB, Used Swap: 0.0 MB"
            return self.handle_receive_data(response)
        if data == 'get_system_info':
            # response = "{'platform': 'Linux', 'processor': '', 'architecture': ('32bit', 'ELF'), 'python_version': '3.9.2'}"
            return self.handle_receive_data_1(response)    
        if data == 'get_os_info':
            # response = {'system': 'Linux', 'node_name': 'pi', 'release': '6.1.21-v7+', 'version': '#1642 SMP Mon Apr 3 17:20:52 BST 2023', 'machine': 'armv71'}
            return self.handle_receive_data_2(response)
        if data == 'get_process_list':
            # response = [{'pid': 1, 'name': 'systemd', 'cpu_percent': 0.0, 'memory_info': 8.6796875}, {'pid': 2, 'name': 'kthreadd', 'cpu_percent': 0.0, 'memory_info': 0.0}]
            return self.handle_receive_data_3(response)
        if data == 'get_cpu_percent':
            return self.handle_receive_data_4(response)
        if data == 'get_temp':
            return self.handle_receive_data_5(response)
        if data == 'cpu_count':
            return self.handle_receive_data_6(response)
        if data == 'cpu_main_core':
            return self.handle_receive_data_7(response)
        if data == 'get_disk_usage':
            return self.handle_receive_data_8(response)
        if data == 'get_date':
            return self.handle_receive_data_9(response)
        if data == 'get_time':
            return self.handle_receive_data_10(response)
        
        client_socket.close()

    # lấy memory info    
    def handle_receive_data(self,response):
        information_string._instance = information_string()
        information_string._instance.update_memory_info(response)
        print(information_string.get_memory_info())

    # lấy sys info
    def handle_receive_data_1(self,response):
        information_string._instance = information_string()
        information_string._instance.update_system_info(response)
        print(information_string.get_system_info())
    
    # lấy os info
    def handle_receive_data_2(self,response):
        information_string._instance = information_string()
        information_string._instance.update_os_info(response)
        print(information_string.get_os_info())
    
    # lấy danh sách process
    def handle_receive_data_3(self,response):
        information_string._instance = information_string()
        information_string._instance.update_process_list(response)
        print(information_string.get_process_list())
    
    # lấy phần trăm cpu
    def handle_receive_data_4(self, response):
        information_string._instance = information_string()
        information_string._instance.update_cpu_percentage(response)
        print(information_string._instance.get_cpu_percentage())
    
    # lấy nhiệt độ
    def handle_receive_data_5(self, response):
        information_string._instance = information_string()
        information_string._instance.update_cpu_temp(response)
        print(information_string._instance.get_cpu_temp())

    # lấy cpu count
    def handle_receive_data_6(self, response):
        information_string._instance = information_string()
        information_string._instance.update_cpu_count(response)
        print(information_string._instance.get_cpu_count())

    # lấy cpu main core
    def handle_receive_data_7(self, response):
        information_string._instance = information_string()
        information_string._instance.update_cpu_main_core (response)
        print(information_string._instance.get_cpu_main_core())

    # lấy cpu main core
    def handle_receive_data_8(self, response):
        information_string._instance = information_string()
        information_string._instance.update_storage (response)
        print(information_string._instance.get_storage())

    def handle_receive_data_9(self, response):
        information_string._instance = information_string()
        information_string._instance.update_date (response)
        print(information_string._instance.get_date())

    def handle_receive_data_10(self, response):
        information_string._instance = information_string()
        information_string._instance.update_time (response)
        print(information_string._instance.get_time())

