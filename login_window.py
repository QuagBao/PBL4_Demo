from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt5.QtCore import pyqtSlot, Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QMouseEvent
import socket
from ui.Loginview_1_UI import Ui_Form
from main_window_3 import MyWindow_3 
from RaspInfo import RaspInfo

class LoginWindow(QWidget):
    loginSignal = pyqtSignal()
    def __init__(self):
        super(LoginWindow, self).__init__()
        # self.main_app = MyWindow_3()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._starPos = None
        self._endPos = None
        self._tracking = False

        # Show login window when starting up (Login: 1, Register: 0)
        self.ui.funcWidget.setCurrentIndex(1)
        
        #hide the frame and background of the app
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.login_button_enabled = True

        self.ui.LoginButton.clicked.disconnect()
        self.ui.LoginButton.clicked.connect(self.on_LoginButton_clicked)
        #phai huy ket noi cu truoc khi ket noi moi
        self.ui.ExitButton.clicked.disconnect()
        self.ui.ExitButton.clicked.connect(self.on_ExitButton_clicked)

    @pyqtSlot()
    def on_ExitButton_clicked(self):
        """
        Function for ExitButton
        """
        msgBox = QMessageBox(self)
        msgBox.setWindowIcon(QIcon("./static/Icons/key-6-16.ico"))
        
        icon = QPixmap("./static/Icons/question-mark-6-16.ico")
        msgBox.setIconPixmap(icon)

        msgBox.setWindowTitle("Thoát ?")
        msgBox.setText("Bạn có muốn thoát không ?")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # Change the button text
        msgBox.button(QMessageBox.Yes).setText("Có")
        msgBox.button(QMessageBox.No).setText("Không")
        
        reply = msgBox.exec_()

        if reply == QMessageBox.Yes:
            self.close()
        else:
            return

    @pyqtSlot()
    def on_CreateButton_clicked(self):
        """
        function for going to register page
        """
        self.ui.funcWidget.setCurrentIndex(0)

    # def check_login(self):
    #     self.show_main_app()
        
    def check_login(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set a timeout for connection attempts

        try:
            # Thử kết nối
            sock.connect((ip, port))
            print("Checking login with IP:", ip, "and port:", port)
            sock.shutdown(socket.SHUT_RDWR)
            self.show_main_app()

        except Exception as e:
            self.show_login_error()
            # Đặt trạng thái của nút là True để kích hoạt lại sau khi hiển thị lỗi
            self.login_button_enabled = True

        finally:
            sock.close()

    def show_main_app(self):
        # self.main_app.show()
        # self.hide()
        self.loginSignal.emit()

    def show_login_error(self):
        QMessageBox.warning(self, "Login Error", "Invalid IP or Port. Please try again.")

    @pyqtSlot()
    def on_LoginButton_clicked(self):
        # Phát tín hiệu để đăng nhập thành công
        # self.loginSignal.emit()
        ip = self.ui.NameDevice1.text()
        port_text = self.ui.IPDevice1.text()
        username_txt=self.ui.username_txt.text()
        password_txt=self.ui.password_txt.text()

        # Kiểm tra xem IP và Port có trống không
        if not ip or not port_text or not username_txt or not password_txt:
            self.show_login_error()
            return
        try:
            port = int(port_text)
        except ValueError:
            self.show_login_error()
            return

        # Kiểm tra trạng thái của nút trước khi thực hiện kết nối
        if not self.login_button_enabled:
            return
        
        # Cập nhật thông tin trong singleton RaspInfo
        RaspInfo().update_config(ip, port,username_txt,password_txt)
        print(f"rasp_ip: {RaspInfo().get_rasp_ip()}, rasp_port: {RaspInfo().get_rasp_port()},user_txt:{RaspInfo().get_rasp_name()},ps_txt:{RaspInfo().get_rasp_password()}")

        # Vô hiệu hóa nút trước khi kiểm tra đăng nhập
        self.login_button_enabled = False

        # Gọi hàm check_login với IP và port đã cung cấp
        self.check_login(ip, port)
        # self.check_login()

    @pyqtSlot()
    def on_BackButton_clicked(self):
        """
        function for going back to login page from register page
        """
        self.ui.funcWidget.setCurrentIndex(1)

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