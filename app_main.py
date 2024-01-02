import sys

from PyQt5.QtWidgets import QApplication

from login_window import LoginWindow
from main_window_3 import MyWindow_3

def setQss(file_path, obj):
    """
    function for reading style file
    """
    with open(file_path, "r", encoding='utf-8') as rf:
        style = rf.read()
        obj.setStyleSheet(style)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    setQss("./static/style.qss", app)

    login_window = LoginWindow()
    main_window_3 = MyWindow_3()
    
    # Khi đăng nhập thành công, hiện cửa sổ chính và ẩn trang đăng nhập
    login_window.loginSignal.connect(main_window_3.show)
    login_window.loginSignal.connect(login_window.hide)

    # Khi đăng xuất thành công, hiện cửa sổ chính và ẩn trang đăng nhập
    main_window_3.logoutSignal_3.connect(main_window_3.hide)
    main_window_3.logoutSignal_3.connect(login_window.show)
    
    login_window.show()
    sys.exit(app.exec_())