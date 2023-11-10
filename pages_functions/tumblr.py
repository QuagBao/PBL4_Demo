from PyQt5.QtWidgets import QWidget
from ui.pages.tumblr_ui import Ui_Form


class Tumblr(QWidget):
    def __init__(self):
        super(Tumblr, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
