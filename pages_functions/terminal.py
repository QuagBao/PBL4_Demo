from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit
from ui.pages.terminal_UI import Ui_Form
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat

import paramiko
import sys
import re
from RaspInfo import RaspInfo

class Terminal(QWidget):
    def __init__(self):
        super(Terminal, self).__init__()
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ssh_connected = False
        self.shell = None
        self.listener_thread = None

        self.ui.input_txt.returnPressed.connect(self.sendCommand)
        self.ui.input_txt.setEnabled(False)
        self.ui.connect_button.clicked.connect(self.connectSSH)
        self.ui.connect_button_2.clicked.connect(self.disconnectSSH)
    
    def sendCommand(self):
        command = self.ui.input_txt.text() + '\n'
        self.shell.send(command)
        self.ui.output_txt.clear()

    def connectSSH(self):
        hostname = str(RaspInfo.get_rasp_ip())
        port = "22"
        username = RaspInfo().get_rasp_name()
        password = RaspInfo().get_rasp_password()
        try:
            self.ssh.connect(hostname, port, username, password)
            self.shell = self.ssh.invoke_shell()
            #tao 1 luong lang nghe de nhan du lieu tu shell SSH va hien thi giao dien
            self.listener_thread = SSHListenerThread(self.shell)
            self.listener_thread.signal.connect(self.appendToTerminal)
            self.listener_thread.start()
            self.ssh_connected = True
            self.ui.output_txt.append('Connected to the server.')
            self.ui.input_txt.setEnabled(True)  # Kích hoạt command_line khi kết nối thành công
        except Exception as e:
            self.ui.output_txt.append(str(e))

    def disconnectSSH(self):
        if self.ssh_connected:
            self.ssh_connected = False
            self.ui.input_txt.setEnabled(False)  # Vô hiệu hóa command_line khi ngắt kết nối
            if self.listener_thread:
                self.listener_thread.stop()  # Sử dụng phương thức stop() để yêu cầu dừng thread
                self.listener_thread.wait()  # Chờ cho đến khi thread kết thúc
            if self.shell:
                self.shell.close()  # Đóng shell SSH
            self.ssh.close()  # Đóng kết nối SSH
            self.ui.output_txt.append('Disconnected from the server.')

    def appendToTerminal(self, message):

        # Remove ANSI escape sequences
        ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
        clean_message = ansi_escape.sub('', message)
        self.ui.output_txt.moveCursor(QTextCursor.End)
        self.ui.output_txt.insertPlainText(clean_message)

# Trong class SSHListenerThread, thêm một biến để kiểm tra tình trạng
        #luong nhan du lieu, no se phat tin hieu signal va gd se cap nhat
class SSHListenerThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self, shell):
        QThread.__init__(self)
        self.shell = shell
        self._is_running = True  # Biến kiểm tra xem thread có đang chạy không
    #kiem tra xem co du lieu moi tu shell  khong, neu co thi gui tin hieu cap nhat gd
    def run(self):
        while self._is_running:
            if self.shell.recv_ready():
                data = self.shell.recv(8192).decode()
                self.signal.emit(data)

    def stop(self):  # Phương thức an toàn để dừng thread
        self._is_running = False

    # Trong class SSHClient, chỉnh sửa hàm disconnectSSH
    def disconnectSSH(self):
        if self.ssh_connected:
            self.ssh_connected = False
            if self.listener_thread:
                self.listener_thread.stop()  # Sử dụng phương thức mới để dừng thread
                self.listener_thread.wait()  # Chờ cho đến khi thread kết thúc
            if self.shell:
                self.shell.close()
            self.ssh.close()
            self.output_box.append('Disconnected from the server.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ssh_client = Terminal()
    ssh_client.show()
    sys.exit(app.exec_())