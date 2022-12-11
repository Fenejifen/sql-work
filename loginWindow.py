"""
存储所有关于登录窗口相关的类
"""
from PySide2.QtUiTools import QUiLoader

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
        self.ui.loginAdminButton.clicked.connect(self.startAdminLogin)
        self.ui.loginStudentButton.clicked.connect(self.startStudentLogin)

    # 按下学生登录按钮后打开学生登录框
    def startStudentLogin(self):
        self.studentLoginWindow = StudentLoginWindow()
        self.studentLoginWindow.ui.show()

    def startAdminLogin(self):
        self.adminLoginWindow = AdminLoginWindow()
        self.adminLoginWindow.ui.show()


class StudentLoginWindow:
    """
    学生登陆窗口
    """

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('./ui/loginStudent.ui')

        # 绑定槽和信号
        # 绑定学生登录按钮
        self.ui.loginButton.clicked.connect(self.login)

    def login(self):
        # 获取用户名密码，然后比对用户名与密码库中的值，符合则登录
        userName = self.ui.userNameEdit.text()
        passWord = self.ui.passWordEdit.text()
        # TODO:这里想着使用一个数据库存储用户名与密码，然后比对，符合登录



class AdminLoginWindow:
    """
    管理员登陆窗口
    """

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('./ui/loginAdmin.ui')

        # 绑定槽和信号
        # 绑定两个登录按钮
        # self.ui.loginAdminButton.clicked.connect(self.startAdminLogin)
        # self.ui.loginStudentButton.clicked.connect(self.startStudentLogin)

    def login(self):
        # 获取用户名密码，然后比对用户名与密码库中的值，符合则登录
        userName = self.ui.userNameEdit.text()
        passWord = self.ui.passWordEdit.text()
        # TODO:这里想着使用一个数据库存储用户名与密码，然后比对，符合登录
