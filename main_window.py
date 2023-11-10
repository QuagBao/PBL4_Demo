from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QPoint, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QIcon, QPixmap

from ui.MainWindow_UI import Ui_MainWindow

from pages_functions.home import Home
from pages_functions.dashboard import Dashboard
from pages_functions.lexus import Lexus
from pages_functions.toyota import Toyota
from pages_functions.youtube import Youtube
from pages_functions.tumblr import Tumblr
from pages_functions.mazda import Mazda


class MyWindow(QMainWindow):
    loginSignal = pyqtSignal()
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Get all objects in window
        self.home_btn = self.ui.home_button
        self.dashboard_btn = self.ui.dashboard_button
        self.lexus_btn = self.ui.lexus_button
        self.toyota_btn = self.ui.toyota_button
        self.mazda_btn = self.ui.mazda_button
        self.youtube_btn = self.ui.youtube_button
        self.tumblr_btn = self.ui.tumblr_button
        ##Create dict for menu buttons and tab windows
        self.menu_btn_dict = {
            self.home_btn: Home,
            self.dashboard_btn: Dashboard,
            self.toyota_btn: Toyota,
            self.lexus_btn: Lexus,
            self.mazda_btn: Mazda,
            self.tumblr_btn: Tumblr,
            self.youtube_btn: Youtube,
        }

        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)
        # show home window when start app
        self.show_home_window()
        #connect signal and slot
        self.home_btn.clicked.connect(self.show_selected_window)
        self.dashboard_btn.clicked.connect(self.show_selected_window)
        self.lexus_btn.clicked.connect(self.show_selected_window)
        self.mazda_btn.clicked.connect(self.show_selected_window)
        self.toyota_btn.clicked.connect(self.show_selected_window)
        self.tumblr_btn.clicked.connect(self.show_selected_window)
        self.youtube_btn.clicked.connect(self.show_selected_window)

    def show_home_window(self):
        result = self.open_tab_flag(self.home_btn)
        self.set_btn_checked(self.home_btn)

        if result[0]:
            self.ui.tabWidget.setCurrentIndex(result[1])
        else:
            tab_title = self.home_btn.text()
            curIndex = self.ui.tabWidget.addTab(Home(), tab_title)
            self.ui.tabWidget.setCurrentIndex(curIndex)
            self.ui.tabWidget.setVisible(True)

    def set_btn_checked(self, btn):
        for button in self.menu_btn_dict.keys():
            if button != btn:
                button.setChecked(False)
            else:
                button.setChecked(True)

    def show_selected_window(self):
        # show selected window
        button = self.sender()
        result = self.open_tab_flag(button.text())
        self.set_btn_checked(button)
        if result[0]:
            self.ui.tabWidget.setCurrentIndex(result[1])
        else:
            tab_title = button.text()
            curIndex = self.ui.tabWidget.addTab(self.menu_btn_dict[button](), tab_title)
            self.ui.tabWidget.setCurrentIndex(curIndex)
            self.ui.tabWidget.setVisible(True)

    def open_tab_flag(self, btn_text):
        # check selected window show or not
        open_tab_count = self.ui.tabWidget.count()
        for i in range(open_tab_count):
            tab_title = self.ui.tabWidget.tabText(i)
            if tab_title == btn_text:
                return True, i
            else:
                continue
        return False,

    def close_tab(self, index):
        self.ui.tabWidget.removeTab(index)
        if self.ui.tabWidget.count() == 0:
            self.ui.toolBox.setCurrentIndex(0)
            self.show_home_window()

    @pyqtSlot()
    def on_ExitButton_clicked(self):
        # Phát tín hiệu để đăng nhập thành công
        self.loginSignal.emit()