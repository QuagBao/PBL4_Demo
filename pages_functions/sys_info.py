from PyQt5.QtWidgets import QWidget
from ui.pages.sys_info_UI import Ui_Form
from information_string import information_string
import re
import json
class System_Information(QWidget):
    def __init__(self):
        super(System_Information, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.handle_receive_data()
        print("da qua sys")
        
    def handle_receive_data(self):
        information_string._instance = information_string()
        result = information_string._instance.get_system_info()
        result_1 = information_string._instance.get_date()
        result_2 = information_string._instance.get_time()
        
        if result is not None:
            #sử dụng hàm chung để lấy các giá trị tương ứng với từ khóa
            platform = self.get_value_from_string(result, 'platform')
            processor = self.get_value_from_string(result, 'processor')
            architecture = self.get_architecture_value(result)
            python_version = self.get_value_from_string(result, 'python_version')
            
            self.ui.txt_hedieuhanh.setText(platform)
            self.ui.txt_platform.setText(platform)
            self.ui.txt_processor.setText(processor)
            self.ui.txt_architecture.setText(architecture)
            self.ui.txt_py_version.setText(python_version)
            self.ui.txt_sysdate.setText(str(result_1))
            self.ui.txt_systime.setText(str(result_2))
    def get_value_from_string(self, data, key):
        try:
            # Xử lý dấu ngoặc đơn trong giá trị 'architecture'
            data = data.replace("(', '", "('").replace("', '", "','").replace("')'", "')")

            # Split the string into lines
            lines = data.split(',')

            # Iterate over each line
            for line in lines:
                # Split each line into key-value pair
                parts = line.split(':')
                if len(parts) == 2:
                    current_key = parts[0].strip().strip("{'")
                    current_value = parts[1].strip().strip("'}")

                    # Kiểm tra xem giá trị có nằm trong dấu ngoặc đơn không
                    if current_value.startswith("(") and current_value.endswith(")"):
                        # Loại bỏ dấu ngoặc đơn
                        current_value = current_value[1:-1]

                    # Check if the current key matches the target key
                    if current_key == key:
                        return current_value

            # If the key is not found in any line
            return "N/A1"
        except Exception as e:
            print(f"Error: {e}")
            return "N/A2"
    
    def get_architecture_value(self, data):
        try:
            # Tìm giá trị nằm trong dấu ngoặc đơn của architecture
            match = re.search(r"'architecture': \('(.*?)', '(.*?)'\)", data)

            # Nếu tìm thấy, trả về giá trị architecture
            if match:
                return f"{match.group(1)}, {match.group(2)}"
            else:
                return "N/A"
        except Exception as e:
            print(f"Error: {e}")
            return "N/A"