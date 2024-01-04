from PyQt5.QtWidgets import QApplication, QTextBrowser, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import QThread, pyqtSignal, QUrl, Qt
from PyQt5.QtGui import QDesktopServices, QTextCursor
import sys
import socket
import re
from ui.pages.network_UI import Ui_Form
from RaspInfo import RaspInfo

class SpeedTestThread(QThread):
    update_signal = pyqtSignal(str)

    def run(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((RaspInfo().get_rasp_ip(), RaspInfo().get_rasp_port()))
            client_socket.send(b'check')
            result = client_socket.recv(1024).decode()
            self.update_signal.emit(result)
        except Exception as e:
            self.update_signal.emit(f"Error: {e}")

class ServerListThread(QThread):
    update_signal = pyqtSignal(str)

    def run(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((RaspInfo().get_rasp_ip(), RaspInfo().get_rasp_port()))
            client_socket.send(b'list_servers')
            result = client_socket.recv(1024).decode()
            self.update_signal.emit(result)
        except Exception as e:
            self.update_signal.emit(f"Error: {e}")

class SpeedTestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.ping_button.clicked.connect(self.ping_server)
        self.ui.result_text_browser.anchorClicked.connect(self.link_clicked)
        self.ui.list_servers_button.clicked.connect(self.list_servers)
        self.ui.check_button.clicked.connect(self.run_speedtest)

    def ping_server(self):
        nmap_command = f"nmap {RaspInfo().get_rasp_ip()}/24"
        print(nmap_command)
        self.send_command(nmap_command)

    def run_speedtest(self):
        self.ui.result_text_browser.clear()
        self.ui.result_text_browser.setPlainText('Testing...')
        self.thread = SpeedTestThread()
        self.thread.update_signal.connect(self.update_result)
        self.thread.start()

    def list_servers(self):
        self.ui.result_text_browser.clear()
        self.ui.result_text_browser.setPlainText('Listing Servers...')
        self.server_list_thread = ServerListThread()
        self.server_list_thread.update_signal.connect(self.update_result)
        self.server_list_thread.start()

    def send_command(self, command):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((RaspInfo().get_rasp_ip(), RaspInfo().get_rasp_port()))
            client_socket.sendall(command.encode())

            response = b""
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                response += data

            response = response.decode()
            print(response)
            self.ui.result_text_browser.append(response)


    def update_result(self, result):
        # Loại bỏ các kí tự không mong muốn và định dạng lại chuỗi văn bản
        result = re.sub(r'%0A', '', result)  # Xoá %0A
        # Gán lại văn bản bình thường trước khi thêm hyperlink
        self.ui.result_text_browser.setPlainText(result)
        # Thêm hyperlink cho tất cả các URL trong kết quả
        urls = re.findall(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            result
        )
        # Đặt cursor về vị trí đầu tiên trong TextBrowser
        cursor = self.ui.result_text_browser.textCursor()
        cursor.movePosition(QTextCursor.Start)
        # Điều chỉnh văn bản để tạo hyperlink chỉ cho URL
        for url in urls:
            # Tìm kiếm và chọn URL hiện tại trong văn bản
            search_pos = self.ui.result_text_browser.find(url)
            if search_pos == -1:  # Nếu không tìm thấy, bỏ qua URL này
                continue
            cursor = self.ui.result_text_browser.textCursor()  # Lấy lại vị trí cursor sau khi tìm kiếm
            cursor.movePosition(QTextCursor.StartOfWord, QTextCursor.KeepAnchor)
            cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
            cursor.insertHtml(f'<a href="{url}">{url}</a>')

    def link_clicked(self, link):
        QDesktopServices.openUrl(QUrl(link))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SpeedTestApp()
    window.show()
    sys.exit(app.exec_())
