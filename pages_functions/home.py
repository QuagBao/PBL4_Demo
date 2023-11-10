import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from ui.pages.home_ui import Ui_Form
import socket
import threading

class Home(QWidget):
    def __init__(self):
        super(Home, self).__init__()
        # self.ui = Ui_Form()
        # self.ui.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Raspberry Pi Control')
        self.setGeometry(100, 100, 400, 300)

        self.temperature_label = QLabel("CPU Temperature:", self)
        self.temperature_entry = QLabel("", self)

        self.get_temp_button = QPushButton("Get Temperature", self)
        self.get_temp_button.clicked.connect(self.get_temperature)

        self.shutdown_reboot_label = QLabel("Shutdown/Reboot:", self)
        self.shutdown_button = QPushButton("Shutdown", self)
        self.reboot_button = QPushButton("Reboot", self)

        self.cpu_label = QLabel("CPU Percentage:", self)
        self.cpu_entry = QLabel("", self)
        self.get_cpu_button = QPushButton("Get CPU Percentage", self)
        self.get_cpu_button.clicked.connect(self.get_cpu_usage)

        self.ram_label = QLabel("RAM Info:", self)
        self.ram_entry = QLabel("", self)
        self.get_ram_button = QPushButton("Get RAM Info", self)
        self.get_ram_button.clicked.connect(self.get_ram_info)

        self.disk_label = QLabel("Disk Info:", self)
        self.disk_entry = QLabel("", self)
        self.get_disk_button = QPushButton("Get Disk Info", self)
        self.get_disk_button.clicked.connect(self.get_disk_info)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.temperature_entry)
        layout.addWidget(self.get_temp_button)

        layout.addWidget(self.shutdown_reboot_label)
        layout.addWidget(self.shutdown_button)
        layout.addWidget(self.reboot_button)

        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_entry)
        layout.addWidget(self.get_cpu_button)

        layout.addWidget(self.ram_label)
        layout.addWidget(self.ram_entry)
        layout.addWidget(self.get_ram_button)

        layout.addWidget(self.disk_label)
        layout.addWidget(self.disk_entry)
        layout.addWidget(self.get_disk_button)

        self.setLayout(layout)

    def get_temperature(self):
        response = self.send_command_to_pi('get_temp')
        self.temperature_entry.setText(response)

    def shutdown(self):
        self.send_command_to_pi('shutdown')

    def reboot(self):
        self.send_command_to_pi('reboot')

    def get_cpu_usage(self):
        response = self.send_command_to_pi('get_cpu_percent')
        self.cpu_entry.setText(response)

    def get_ram_info(self):
        response = self.send_command_to_pi('get_ram_info')
        self.ram_entry.setText(response)

    def get_disk_info(self):
        response = self.send_command_to_pi('get_disk_info')
        self.disk_entry.setText(response)

    def send_command_to_pi(self, command):
        SERVER_HOST = '192.168.1.11'
        SERVER_PORT = 5000

        with socket.socket() as client_socket:
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            client_socket.send(command.encode())
            response = client_socket.recv(1024).decode()

        return response

# if __name__ == '__main__':
#     raspberry_pi_app = Home()

#     def run_qt():
#         app = QApplication(sys.argv)
#         raspberry_pi_app.show()
#         sys.exit(app.exec_())

#     qt_thread = threading.Thread(target=run_qt)
#     qt_thread.start()