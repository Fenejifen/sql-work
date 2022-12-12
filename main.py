from PySide2.QtWidgets import QApplication

import login_window

if __name__ == "__main__":
    app = QApplication()
    mainWindow = login_window.MainLoginWindow()
    mainWindow.ui.show()
    app.exec_()
