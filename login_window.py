from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt5.QtCore import pyqtSlot, Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QMouseEvent

from ui.LoginView_UI import Ui_Form
from main_window import MyWindow 

class LoginWindow(QWidget):
    loginSignal = pyqtSignal()
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._starPos = None
        self._endPos = None
        self._tracking = False

        # Show login window when starting up (Login: 1, Register: 0)
        self.ui.funcWidget.setCurrentIndex(1)
        
        #hide the frame and background of the app
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    @pyqtSlot()
    def on_ExitButton_clicked(self):
        """
        Function for ExitButton
        """
        msgBox = QMessageBox(self)
        msgBox.setWindowIcon(QIcon("./static/Icons/key-6-16.ico"))
        
        icon = QPixmap("./static/Icons/question-mark-6-16.ico")
        msgBox.setIconPixmap(icon)

        msgBox.setWindowTitle("Thoát ?")
        msgBox.setText("Bạn có muốn thoát không ?")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # Change the button text
        msgBox.button(QMessageBox.Yes).setText("Có")
        msgBox.button(QMessageBox.No).setText("Không")
        
        reply = msgBox.exec_()

        if reply == QMessageBox.Yes:
            self.close()
        else:
            return

    @pyqtSlot()
    def on_CreateButton_clicked(self):
        """
        function for going to register page
        """
        self.ui.funcWidget.setCurrentIndex(0)

    @pyqtSlot()
    def on_LoginButton_clicked(self):
        # Phát tín hiệu để đăng nhập thành công
        self.loginSignal.emit()

    @pyqtSlot()
    def on_BackButton_clicked(self):
        """
        function for going back to login page from register page
        """
        self.ui.funcWidget.setCurrentIndex(1)

    ## TODO: make the window movable after hide window frame
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if self._tracking:
            self._endPos = a0.pos() - self._starPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self._starPos = QPoint(a0.x(), a0.y())
            self._tracking = True

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self._tracking = False
            self._starPos = None
            self._endPos = None