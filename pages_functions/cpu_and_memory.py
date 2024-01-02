from PyQt5.QtWidgets import QWidget, QApplication
from ui.pages.cpu_and_memory_UI import Ui_Form
from information_string import information_string
import sys
import json
import os  # Thêm thư viện os để kiểm tra sự tồn tại của file
import re

# from PySide2 import *

# #IMPORT PYSIDE2EXTN WIDGET YOU USED IN THE QTDESIGNER FOR DESIGNING.
# from PySide2extn.RoundProgressBar import roundProgressBar
import RoundProcessBar

class CPU_and_Memory(QWidget):

    def __init__(self):
        super(CPU_and_Memory, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.handle_receive_data()
        print("da qua cpu")
        
    def handle_receive_data(self):
        information_string._instance = information_string()
        result = information_string._instance.get_memory_info()
        result_1 = information_string._instance.get_cpu_percentage()
        result_2 = information_string._instance.get_cpu_temp()
        result_3 = information_string._instance.get_cpu_count()
        result_4 = information_string._instance.get_cpu_main_core()
        if result is not None or result_1 is not None or result_2 is not None or result_3 is not None or result_4 is not None:
            # Sử dụng hàm chung để lấy trường dữ liệu tương 
            self.ui.txt_cpu_temp.setText(result_2 + " °C")
            self.ui.txt_cpu_per.setText(result_1)
            self.ui.txt_cpu_count.setText(result_3)
            self.ui.txt_cpu_main_core.setText(result_4)

            available_ram = self.extract_value_by_key(result, "Available RAM")
            total_ram = self.extract_value_by_key(result, "Total RAM")
            used_ram = self.extract_used_ram(result)

            total_swap = self.extract_value_by_key(result, "Total Swap")
            used_swap = self.extract_value_by_key(result, "Used Swap")
            free_swap = self.minus_float(total_swap, used_swap)
            ram_usage = self.per_float(used_ram, total_ram)

            self.ui.txt_total_ram.setText(total_ram+" MB")
            self.ui.txt_available_ram.setText(available_ram+" MB")
            self.ui.txt_used_ram.setText(used_ram+" MB")
            self.ui.txt_ram_usage.setText(ram_usage+"%")
            
            self.ui.txt_total_swap.setText(total_swap+" MB")
            self.ui.txt_used_swap.setText(used_swap+" MB")
            self.ui.txt_free_swap.setText(free_swap+" MB")

            # Thiết lập biểu đồ 
            # Biểu đồ phần trăm CPU
            # self.ui.cpu_percentage.rpb_setMaximum(100) 
            self.ui.cpu_percentage.rpb_setInitialPos('West')
            self.ui.cpu_percentage.rpb_setBarStyle("Hybrid2")
            self.ui.cpu_percentage.rpb_setValue( float(result_1))
            self.ui.cpu_percentage.rpb_setLineCap('RoundCap')
            self.ui.cpu_percentage.rpb_setTextColor((61,86,115))
            self.ui.cpu_percentage.rpb_setPieColor((105,145,181))
            self.ui.cpu_percentage.rpb_setPieRatio(0.9)
            
            # Biểu đồ của RAM
            self.ui.cpu_ram.spb_setNoProgressBar(2)
            self.ui.cpu_ram.spb_setMinimum( (float(0),float(0)) )
            self.ui.cpu_ram.spb_setMaximum( (float(total_ram), float(total_ram)) )
            self.ui.cpu_ram.spb_setValue( (float(available_ram), float(used_ram)) )
            self.ui.cpu_ram.spb_lineColor(((41,122,110), (105,145,181)))
            self.ui.cpu_ram.spb_setInitialPos(('West', 'West'))
            self.ui.cpu_ram.spb_lineWidth(15)
            self.ui.cpu_ram.spb_setGap(15)
            self.ui.cpu_ram.spb_lineStyle(('SolidLine', 'SolidLine'))
            self.ui.cpu_ram.spb_lineCap(('RoundCap', 'RoundCap'))
            self.ui.cpu_ram.spb_setPathHidden(True)
            # Biểu đồ của SWAP
            
    def extract_used_ram(self, data):
        try:
            # Biểu thức chính quy để tìm giá trị của "Used RAM"
            used_ram_pattern = re.compile(r'Used RAM: ([^,]+)')

            # Tìm match trong chuỗi
            used_ram_match = used_ram_pattern.search(data)

            # Nếu tìm thấy "Used RAM", trả về giá trị trích xuất
            if used_ram_match:
                used_ram_value = used_ram_match.group(1).strip()

                # Tìm match của "Total Swap"
                total_swap_pattern = re.compile(r'Total Swap: ([^,]+)')
                total_swap_match = total_swap_pattern.search(data)

                # Nếu tìm thấy "Total Swap", loại bỏ giá trị "Total Swap" từ "Used RAM"
                if total_swap_match:
                    total_swap_value = total_swap_match.group(1).strip()
                    used_ram_value = total_swap_pattern.sub('', used_ram_value).strip()

                # Loại bỏ chữ "MB" và chuyển đổi sang số với 2 chữ số thập phân
                used_ram_value = round(float(used_ram_value.replace("MB", "")), 2)

                return f"{used_ram_value:.2f}"
            else:
                return "N/A"
        except Exception as e:
            print(f"Lỗi: {e}")
            return "N/A"
        
    def extract_value_by_key(self, data, key):
        try:
            # Biểu thức chính quy để tìm giá trị của key
            pattern = re.compile(fr'\b{key}\b: ([^,]+)')
            # Tìm match trong chuỗi
            match = pattern.search(data)
            # Nếu tìm thấy match, trả về giá trị trích xuất
            if match:
                value = match.group(1).strip()
                # Loại bỏ chữ "MB" và chuyển đổi sang số với 2 chữ số thập phân
                value = round(float(value.replace("MB", "")), 2)
                return f"{value:.2f}"
            else:
                # Nếu không tìm thấy key trong chuỗi
                return "N/A"
        except Exception as e:
            print(f"Lỗi: {e}")
            return "N/A"
        
    def minus_float(self, data, data1):
        try:
            # Hàm để loại bỏ chữ "MB" từ chuỗi
            def remove_mb(s):
                return s.replace("MB", "").strip()

            # Kiểm tra nếu một trong hai chuỗi là "N/A"
            if data == "N/A" or data1 == "N/A":
                print("Loi")
                return "Loi"

            # Loại bỏ "MB" và chuyển đổi sang kiểu số
            s1 = float(remove_mb(data))
            s2 = float(remove_mb(data1))
            remaining = s1 - s2
            return f"{remaining:.2f} "
        except ValueError:
            return "N/A"
        
    def per_float(self, data, data1):
        try:
            # Hàm để loại bỏ chữ "MB" từ chuỗi
            def remove_mb(s):
                return s.replace("MB", "").strip()

            # Kiểm tra nếu một trong hai chuỗi là "N/A"
            if data == "N/A" or data1 == "N/A":
                print("Loi")
                return "Loi"

            # Loại bỏ "MB" và chuyển đổi sang kiểu số
            s1 = float(remove_mb(data))
            s2 = float(remove_mb(data1))
            remaining = s1/s2 * 100
            return f"{remaining:.2f}"
        except ValueError:
            return "N/A"    
        
if __name__ == '__main__':
    app = QApplication([])
    lexus_app = CPU_and_Memory()
    lexus_app.show()
    sys.exit(app.exec_())
