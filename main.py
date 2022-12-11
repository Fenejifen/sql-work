import sys
from PySide2.QtWidgets import QApplication, QMessageBox
from loginWindow import MainLoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainLoginWindow()
    mainWindow.ui.show()
    app.exec_()
