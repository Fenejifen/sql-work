from PySide2.QtWidgets import QApplication

from loginWindow import MainLoginWindow

if __name__ == "__main__":
    app = QApplication()
    mainWindow = MainLoginWindow()
    mainWindow.ui.show()
    app.exec_()
