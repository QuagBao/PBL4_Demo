from PyQt5.QtWidgets import QWidget
from ui.pages.os_info_UI import Ui_Form
from information_string import information_string
import re

class OS_Info(QWidget):
    def __init__(self):
        super(OS_Info, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.handle_receive_data()
        print("da qua os")

    def handle_receive_data(self):
        information_string._instance = information_string()
        result = information_string._instance.get_os_info()
        result_1 = information_string._instance.get_date()
        result_2 = information_string._instance.get_time()
        print(result_1,result_2)
        if result is not None:
            #sử dụng hàm chung để lấy các giá trị tương ứng với từ khóa
            system = self.get_value_from_string(result, 'system')
            node_name = self.get_value_from_string(result, 'node_name')
            release = self.get_value_from_string(result, 'release')
            version = self.get_version_from_string(result)

            machine = self.get_value_from_string(result, 'machine')

            self.ui.txt_system.setText(system)
            self.ui.txt_node_name.setText(node_name.capitalize())
            self.ui.txt_release.setText(release)
            self.ui.txt_version.setText(version)
            self.ui.txt_machine.setText(machine.upper())
            self.ui.txt_sysdate.setText(str(result_1))
            self.ui.txt_systime.setText(str(result_2))
    def get_value_from_string(self, data, key):
        try:
            # Chuyển đối tượng từ điển thành chuỗi
            data_str = str(data)

            # Xử lý dấu ngoặc đơn trong giá trị 'architecture'
            data_str = data_str.replace("(', '", "('").replace("', '", "','").replace("')'", "')")

            # Split the string into lines
            lines = data_str.split(',')

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
    
    def get_version_from_string(self,data):
        try:
            # Biểu thức chính quy để tìm giá trị của khóa "version"
            version_pattern = re.compile(r"'version': '([^']+)'")

            # Chuyển đối tượng đầu vào thành chuỗi nếu nó không phải là chuỗi
            data_str = str(data)

            # Tìm match trong chuỗi
            match = version_pattern.search(data_str)

            # Nếu tìm thấy match, trả về giá trị trích xuất
            if match:
                return match.group(1).strip()
            else:
                return "N/A"
        except Exception as e:
            print(f"Error: {e}")
            return "N/A"