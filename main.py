import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    icon = QIcon(":/commont/image/logo.ico")
    window.setWindowIcon(icon)
    window.show()
    sys.exit(app.exec_())
