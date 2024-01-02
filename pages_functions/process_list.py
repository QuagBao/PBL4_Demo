from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QTimer
import socket
import sys
import paramiko
from PyQt5.QtWidgets import QApplication
from ui.pages.process_list_UI import Ui_Form
from RaspInfo import RaspInfo

class Process_List(QWidget):
    def __init__(self):
        super(Process_List, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        print("da qua process list")
        self.client_socket = None
        self.server_address = None
        self.table_widget = None
         
        self.init_network()
        
        # hello
        self.ui.kill_btn.clicked.connect(self.kill_selected_task)
        self.ui.refresh_btn.clicked.connect(self.refresh_tasks)
        self.ui.search_btn.clicked.connect(self.search_tasks)
    def init_network(self):
        try:
            self.server_address = (RaspInfo().get_rasp_ip(), RaspInfo().get_rasp_port())
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(self.server_address)
            self.refresh_tasks()
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def search_tasks(self):
        search_term = self.ui.search_txt.text().lower()
        if not search_term:
            print("Please enter a search term.")
            return
        try:
            with paramiko.SSHClient() as ssh_client:
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                # hostname=RaspInfo().get_rasp_ip(), username=RaspInfo().get_rasp_name(), password=RaspInfo().get_rasp_password()
                ssh_client.connect(hostname=RaspInfo().get_rasp_ip(), username=RaspInfo().get_rasp_name(), password=RaspInfo().get_rasp_password())
                stdin, stdout, stderr = ssh_client.exec_command(f"ps -A | grep '{search_term}'")
                tasks = stdout.readlines()
                self.fill_table(tasks)
        except paramiko.SSHException as ssh_exception:
            print(f"SSHException: {ssh_exception}")
        except Exception as e:
            print(f"Error searching tasks: {e}")


    def fill_table(self, task_lines):
        self.ui.tableWidget.setRowCount(0)
        for task_info in task_lines:
            task_data = task_info.split()
            if task_data:  # Check if the line is not empty
                row_position = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(row_position)
                for col, value in enumerate(task_data[:4]):  # Limit to 4 columns for 'PID', 'TTY', 'TIME', 'CMD'
                    item = QTableWidgetItem(value)
                    self.ui.tableWidget.setItem(row_position, col, item)

    def refresh_tasks(self):
        try:
            self.client_socket.send('list'.encode('utf-8'))
            task_list_data = ""
            while True:
                part = self.client_socket.recv(4096).decode('utf-8')
                task_list_data += part
               
                if not part:
                    break  # Kết thúc vòng lặp khi dữ liệu đã kết thúc
            task_lines = task_list_data.strip().split('\n')
            # self.ui.tableWidget.setRowCount(0)
            self.fill_table(task_lines[1:])  # Gọi hàm fill_table để điền dữ liệu vào bảng

            # for task_info in task_lines[1:]:
            #     task_data = task_info.split()
            #     row_position = self.ui.tableWidget.rowCount()
            #     self.ui.tableWidget.insertRow(row_position)
            #     for col, value in enumerate(task_data):
            #         item = QTableWidgetItem(value)
            #         self.ui.tableWidget.setItem(row_position, col, item)
            # if self.ui.tableWidget.rowCount() > 0:
            #     self.ui.tableWidget.setCurrentItem(self.ui.tableWidget.item(0, 0))
        except BrokenPipeError:
            print("BrokenPipeError: Kết nối bị đứt. Đang thử kết nối lại...")
            self.client_socket.close()
            self.init_network()  # Re-initialize network connection.
        except Exception as e:
            print(f"Error refreshing tasks: {e}")


    def kill_selected_task(self):
        try:
            selected_row = self.ui.tableWidget.currentRow()
            pid_item = self.ui.tableWidget.item(selected_row, 0)
            selected_pid = pid_item.text()
            if selected_pid:
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=RaspInfo().get_rasp_ip(), username=RaspInfo().get_rasp_name(), password=RaspInfo().get_rasp_password())
                stdin, stdout, stderr = ssh_client.exec_command(f'kill {selected_pid}')
                print(stdout.read())
                print(stderr.read())
                ssh_client.close()  # Đóng kết nối SSH ngay sau khi thực hiện lệnh kill
                self.refresh_tasks()

        except paramiko.SSHException as ssh_exception:
            print(f"SSHException: {ssh_exception}")
            self.reconnect_ssh()  # Thử kết nối lại nếu có lỗi SSH
        except BrokenPipeError:
            print("BrokenPipeError: Kết nối bị đứt. Đang thử kết nối lại...")
            self.client_socket.close()
            self.init_network()  # Re-initialize network connection.
        except Exception as e:
            print(f"Error killing selected task: {e}")

    def reconnect_ssh(self):
        try:
            self.kill_ssh_client.close()
            self.kill_ssh_client.connect(hostname=RaspInfo().get_rasp_ip(),username=RaspInfo().get_rasp_name(), password=RaspInfo().get_rasp_password())
        except Exception as e:
            print(f"Error reconnecting SSH: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_app = Process_List()
    client_app.show()
    sys.exit(app.exec_())
