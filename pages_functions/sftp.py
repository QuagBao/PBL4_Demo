import sys
import paramiko
from RaspInfo import RaspInfo
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTreeView, QVBoxLayout, QDialog,
                             QLabel, QWidget, QPushButton, QMessageBox, QFileDialog, QLineEdit)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QCoreApplication

import pyperclip

from ui.pages.sftp_UI import Ui_Form


class SFTPUploader(QDialog):
    def __init__(self):
        super().__init__()
        self.selected_file = None
        
        self.initUI()

   

    def initUI(self):
        self.setWindowTitle('SFTP File Uploader')
        self.setGeometry(100, 100, 300, 150)
        layout = QVBoxLayout()

        self.choose_file_button = QPushButton('Choose File', self)
        self.choose_file_button.clicked.connect(self.choose_file)
        layout.addWidget(self.choose_file_button)

        # Button to upload the file
        self.upload_button = QPushButton('Upload', self)
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)

        self.setLayout(layout)

    def choose_file(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFile)
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.selected_file= filenames[0]
            QMessageBox.information(self, 'File Selected', f'Selected file: {self.selected_file}')

    def upload_file(self):

        hostname = RaspInfo().get_rasp_ip()

        username = RaspInfo().get_rasp_name()

        password = RaspInfo().get_rasp_password()

        if self.selected_file:

            try:

                transport = paramiko.Transport((hostname, 22))

                transport.connect(username=username, password=password)

                sftp = paramiko.SFTPClient.from_transport(transport)

                target_path = f'/home/{username}/{self.selected_file.split("/")[-1]}'

                sftp.put(self.selected_file, target_path)

                sftp.close()

                transport.close()

                QMessageBox.information(self, 'Success', 'The file has been uploaded successfully.')

            except Exception as e:

                QMessageBox.critical(self, 'Error', f'An error occurred while uploading the file: {str(e)}')

        else:

            QMessageBox.warning(self, 'Warning', 'Please select a file to upload.')


class SFTP(QWidget):
    def __init__(self):
        super().__init__()
        self.current_path = ''
        self.previous_paths = []
        self.ssh_client = self.connect_to_host(RaspInfo().get_rasp_ip(), RaspInfo().get_rasp_name(), RaspInfo().get_rasp_password())
        # self.initUI()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Home button
        self.ui.move_up_btn.clicked.connect(self.go_home)
        
        # Back button
        self.ui.move_down_btn.clicked.connect(self.go_back)

        # Copy Path button
        self.ui.new_file_btn.clicked.connect(self.copy_path)

        # Disconnect button
        self.ui.delete_file_btn.clicked.connect(self.disconnect_from_host)

        # Send File button
        self.ui.send_file_btn.clicked.connect(self.send_file_dialog)

        # Receive File button
        self.ui.receive_file_btn.clicked.connect(self.receive_file)

        # Connect double-click signal
        self.ui.files.doubleClicked.connect(self.on_double_click)

        #Set the model
        self.model = QStandardItemModel()
        self.ui.files.setModel(self.model)

        # Initialize the home folder view
        self.go_home()

    def connect_to_host(self, ip, username, password):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, username=username, password=password)
            return client
        except paramiko.SSHException as e:
            QMessageBox.critical(self, 'Connection Failed', f"Failed to connect to the host: {e}")
            sys.exit(-1)        

    def send_file_dialog(self):
        dialog = SFTPUploader()
        dialog.exec_()

    def on_double_click(self, index):
        item = self.model.itemFromIndex(index)
        path = item.data()
        try:
            with self.ssh_client.open_sftp() as sftp:
                if sftp.stat(path).st_mode & 0o40000:  # Check if it's a folder
                    self.previous_paths.append(self.current_path)
                    self.populate_tree(path)
                else:  # It's a file
                    self.show_file_info(path)
        except Exception as e:
            QMessageBox.warning(self, 'Operation Failed', f"Operation failed: {e}")

    def show_file_info(self, path):
        self.ui.path_label.setText(f"This is a file: {path}")

    def populate_tree(self, path):
        self.current_path = path
        self.ui.path_label.setText(f"Current Path: {path}")
        self.model.clear()
        try:
            with self.ssh_client.open_sftp() as sftp:
                for entry in sftp.listdir_attr(path):
                    entry_name = entry.filename
                    attrs = entry.st_mode  # Lấy thuộc tính của từng mục
                    if attrs & 0o40000:  # Check if it's a folder
                        entry_name += "/"
                    item = QStandardItem(entry_name)
                    item.setData(f"{path}/{entry_name}".rstrip('/'))
                    self.model.appendRow(item)
        except Exception as e:
            QMessageBox.warning(self, 'Operation Failed', f"Operation failed: {e}")

    def disconnect_from_host(self):
        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None
            self.model.clear()
            QMessageBox.information(self, 'Disconnected', 'The SSH connection was closed successfully.')

    def receive_file(self):
        text = self.ui.path_label.text()
        if text.startswith('Current Path: '):
            QMessageBox.warning(self, 'Invalid Path', 'Please select a file, not a folder.')
            return
        elif text.startswith('This is a file: '):
            file_path = text.replace('This is a file: ', '')
            save_path = QFileDialog.getSaveFileName(self, 'Save File', file_path.split('/')[-1])[0]
            if save_path:
                self.download_file(file_path, save_path)

    def download_file(self, file_path, save_path):
        try:
            with self.ssh_client.open_sftp() as sftp:
                sftp.get(file_path, save_path)
                QMessageBox.information(self, 'File Received', f"File downloaded to {save_path}.")
        except Exception as e:
            QMessageBox.warning(self, 'Download Failed', f"Failed to download file: {e}")

    def go_home(self):
        self.populate_tree('/home')

    def go_back(self):
        if self.previous_paths:
            previous_path = self.previous_paths.pop()
            self.populate_tree(previous_path)

    def copy_path(self):
        text = self.ui.path_label.text()
        if text.startswith('Current Path: '):
            text = text.replace('Current Path: ', '')
        elif text.startswith('This is a file: '):
            text = text.replace('This is a file: ', '')
        pyperclip.copy(text)
        QMessageBox.information(self, 'Path Copied', f"Path '{text}' copied to clipboard.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SFTP()
    ex.show()
    sys.exit(app.exec_())
