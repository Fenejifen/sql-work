"""
存储所有关于登录窗口相关的类
"""
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMessageBox, QGraphicsScene, QGraphicsPixmapItem

from sql import SQL


class MainLoginWindow:
    """
    登录窗口主界面
    """

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('./ui/loginMain.ui')

        # 绑定槽和信号
        # 绑定两个登录按钮
        self.ui.loginAdminButton.clicked.connect(self.start_admin_login)
        self.ui.loginStudentButton.clicked.connect(self.start_student_login)

    # 按下学生登录按钮后打开学生登录框
    def start_student_login(self):
        self.studentLoginWindow = StudentLoginWindow()
        self.studentLoginWindow.ui.show()
        self.ui.close()

    def start_admin_login(self):
        self.adminLoginWindow = AdminLoginWindow()
        self.adminLoginWindow.ui.show()
        self.ui.close()


class StudentLoginWindow:
    """
    学生登陆窗口
    """

    def __init__(self):
        self.ui = QUiLoader().load('./ui/loginStudent.ui')

        # 绑定学生登录按钮
        self.ui.loginButton.clicked.connect(self.login)

    def login(self):
        # 获取用户名密码，然后比对用户名与密码库中的值，符合则登录
        user_name = self.ui.userNameEdit.text()
        pass_word = self.ui.passWordEdit.text()
        if SQL.check_login(user_name, pass_word, True):
            # 登录成功，进入新界面
            self.studentMainWindow = StudentMainWindow(user_name)
            self.studentMainWindow.ui.show()
            self.ui.close()
        else:
            # 登录失败，
            QMessageBox.about(self.ui,
                              '登录失败',
                              '用户名或密码错误'
                              )


class AdminLoginWindow:
    """
    管理员登陆窗口
    """

    def __init__(self):
        # 载入UI界面
        self.ui = QUiLoader().load('./ui/loginAdmin.ui')

        # 绑定管理员登录按钮
        self.ui.loginButton.clicked.connect(self.login)

    def login(self):
        # 获取用户名密码，然后比对用户名与密码库中的值，符合则登录
        user_name = self.ui.userNameEdit.text()
        pass_word = self.ui.passWordEdit.text()
        if SQL.check_login(user_name, pass_word, False):
            # 登录成功，进入新界面
            self.adminMainWindow = AdminMainWindow()
            self.adminMainWindow.ui.show()
            self.ui.close()
        else:
            # 登录失败，
            QMessageBox.about(self.ui,
                              '登录失败',
                              '用户名或密码错误'
                              )


class StudentMainWindow:
    """
    学生操作主界面
    """

    def __init__(self, user_name):
        self.ui = QUiLoader().load('./ui/studentMain.ui')
        self.user_name = user_name
        self.get_personal_data()

    def get_personal_data(self):
        # 得到个人信息，显示在学生操作界面右上角
        information = SQL.get_students_personal_data(self.user_name, True)
        # TODO:删除调试代码
        print(information)
        self.ui.SName.setText(information[0])
        self.ui.SGender.setText(information[1])
        self.ui.SAge.setText(str(information[2]))
        self.ui.SClass.setText(information[3])
        self.ui.UserName.setText(information[4])
        self.ui.Sdept.setText(information[5])
        self.ui.SRemain.setText(str(information[6]))

        # 左上角显示图片的一大段代码
        self.image_qt = QImage('./photo/' + f'{self.user_name}' + '.jpg')
        pic = QGraphicsPixmapItem()
        pic.setPixmap(QPixmap.fromImage(self.image_qt))
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 0, 0)
        self.scene.addItem(pic)
        self.ui.profilePhoto.setScene(self.scene)


class AdminMainWindow:
    """
    管理员操作主界面
    """

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('./ui/adminMain.ui')

        # 绑定槽和信号
        # 绑定两个登录按钮
        # self.ui.loginAdminButton.clicked.connect(self.startAdminLogin)
        # self.ui.loginStudentButton.clicked.connect(self.startStudentLogin)
