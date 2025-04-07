from PyQt5.QtWidgets import QWidget, QVBoxLayout

from ui.sidebar import Sidebar


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("图片处理")
        self.setGeometry(200, 200, 1000, 600)
        layout = QVBoxLayout()
        self.sidebar = Sidebar(self)
        layout.addWidget(self.sidebar)
        self.setLayout(layout)

