from PyQt5.QtWidgets import QWidget
from ui.pages.file_list_UI import Ui_Form
from information_string import information_string

class File_List(QWidget):
    def __init__(self):
        super(File_List, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
    #     print("da qua day")
    #     self.handle_receive_data()
    #     print("da qua day")
        
    # def handle_receive_data(self):
    #     information_string._instance = information_string()
    #     result = information_string._instance.get_string_1()
    #     print(result)
    #     self.ui.result_text.setText(result)