"""
存储所有关于登录窗口相关的类
"""
from PySide2.QtGui import QImage, QPixmap, QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMessageBox, QGraphicsScene, QGraphicsPixmapItem, QTableWidgetItem

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
        self.ui.backButton.clicked.connect(self.jump_to_back)

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

    def jump_to_back(self):
        # 跳转到上一层
        self.back = MainLoginWindow()
        self.back.ui.show()
        self.ui.close()


class AdminLoginWindow:
    """
    管理员登陆窗口
    """

    def __init__(self):
        # 载入UI界面
        self.ui = QUiLoader().load('./ui/loginAdmin.ui')

        # 绑定管理员登录按钮
        self.ui.loginButton.clicked.connect(self.login)
        self.ui.backButton.clicked.connect(self.jump_to_back)

    def login(self):
        # 获取用户名密码，然后比对用户名与密码库中的值，符合则登录
        user_name = self.ui.userNameEdit.text()
        pass_word = self.ui.passWordEdit.text()
        if SQL.check_login(user_name, pass_word, False):
            # 登录成功，进入新界面
            self.adminMainWindow = AdminMainWindow(user_name)
            self.adminMainWindow.ui.show()
            self.ui.close()
        else:
            # 登录失败，
            QMessageBox.about(self.ui,
                              '登录失败',
                              '用户名或密码错误'
                              )

    def jump_to_back(self):
        # 跳转到上一层
        self.back = MainLoginWindow()
        self.back.ui.show()
        self.ui.close()

class StudentMainWindow:
    """
    学生操作主界面
    """

    def __init__(self, user_name):
        self.ui = QUiLoader().load('./ui/studentMain.ui')
        self.user_name = user_name
        self.get_personal_data()

        # 绑定操作按钮
        self.ui.queryAndBorrow.clicked.connect(self.jump_to_queryAndBorrow)
        self.ui.renewAndReturn.clicked.connect(self.jump_to_renewAndReturn)
        self.ui.backButton.clicked.connect(self.jump_to_back)

    def jump_to_back(self):
        # 跳转到上一层
        self.back = StudentLoginWindow()
        self.back.ui.show()
        self.ui.close()

    def jump_to_renewAndReturn(self):
        self.renewAndReturn = renewAndReturn(self.user_name)
        self.renewAndReturn.ui.show()
        self.ui.close()

    def jump_to_queryAndBorrow(self):
        self.queryAndBorrow = queryAndBorrowWindow(self.user_name)
        self.queryAndBorrow.ui.show()
        self.ui.close()

    def get_personal_data(self):
        # 得到个人信息，显示在学生操作界面右上角
        information = SQL.get_students_personal_data(self.user_name, True)
        # TODO:删除调试代码
        print(information)
        self.ui.Name.setText(information[0])
        self.ui.Gender.setText(information[1])
        self.ui.Age.setText(str(information[2]))
        self.ui.Class.setText(information[3])
        self.ui.UserName.setText(information[4])
        self.ui.Dept.setText(information[5])
        self.ui.Remain.setText(str(information[6]))

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

    def __init__(self, user_name):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('./ui/adminMain.ui')
        self.user_name = user_name
        self.get_personal_data()

        # 绑定操作按钮
        # TODO:绑定管理员相关操作
        # self.ui.bookManagement.clicked.connect()
        # self.ui.studentManagement.clicked.connect()
        # self.ui.confirmationManagement.clicked.connect()
        self.ui.backButton.clicked.connect(self.jump_to_back)

    def jump_to_back(self):
        # 跳转到上一层
        self.back = AdminLoginWindow()
        self.back.ui.show()
        self.ui.close()

    def get_personal_data(self):
        # 得到个人信息，显示在学生操作界面右上角
        information = SQL.get_students_personal_data(self.user_name, False)
        # TODO:删除调试代码
        print(information)
        self.ui.Name.setText(information[0])
        self.ui.Gender.setText(information[1])
        self.ui.Age.setText(str(information[2]))
        self.ui.UserName.setText(information[3])

        # 左上角显示图片的一大段代码
        self.image_qt = QImage('./photo/' + f'{self.user_name}' + '.jpg')
        pic = QGraphicsPixmapItem()
        pic.setPixmap(QPixmap.fromImage(self.image_qt))
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 0, 0)
        self.scene.addItem(pic)
        self.ui.profilePhoto.setScene(self.scene)


class queryAndBorrowWindow:
    """
    查询与借阅界面
    """

    def __init__(self, user_name):
        self.ui = QUiLoader().load('./ui/queryAndBorrow.ui')
        self.user_name = user_name

        # 设置搜索框图标
        self.ui.searchButton.setIcon(QIcon('./image/search.jpeg'))
        # 绑定操作按钮
        self.ui.searchButton.clicked.connect(self.search_book_by_name)
        self.ui.borrowButton.clicked.connect(self.borrow_the_book)
        self.ui.backButton.clicked.connect(self.jump_to_back)

    def borrow_the_book(self):
        # 按下借阅框后借阅当前选中行的书籍,并视是否借阅成功而执行各种操作
        current_row = self.ui.informationTable.currentRow()
        isbn = self.ui.informationTable.item(current_row, 0).text()
        # TODO: 根据ISBN与user_name进行借阅相关操作
        print(isbn)

    def search_book_by_name(self):
        # TODO:加入模糊搜索
        # 按下搜索按钮后获得信息并输出至信息框
        book_name = self.ui.searchEdit.text()
        book_information = SQL.search_book_by_name(book_name)
        self.ui.searchInformationLabel.setText(f"共搜索到了{len(book_information)}个结果")
        self.ui.informationTable.clearContents()
        for i, row_information in enumerate(book_information):
            self.ui.informationTable.insertRow(i)
            for j, col_information in enumerate(row_information):
                item = QTableWidgetItem(str(col_information))
                self.ui.informationTable.setItem(i, j, item)

    def jump_to_back(self):
        # 跳转到上一层
        self.back = StudentMainWindow(self.user_name)
        self.back.ui.show()
        self.ui.close()


class renewAndReturn:
    """
    续借与归还界面
    """

    def __init__(self, user_name):
        self.ui = QUiLoader().load('./ui/renewAndReturn.ui')
        self.user_name = user_name

        # 获取界面相关信息
        self.get_borrow_information()

        # 绑定操作按钮
        self.ui.renewButton.clicked.connect(self.renew_the_book)
        self.ui.returnButton.clicked.connect(self.return_the_book)
        self.ui.backButton.clicked.connect(self.jump_to_back)

    def get_borrow_information(self):
        book_information = SQL.get_borrow_information(self.user_name)
        self.ui.borrowInformationLabel.setText(f"当前共借阅{len(book_information)}本书籍")
        for i, row_information in enumerate(book_information):
            self.ui.informationTable.insertRow(i)
            for j, col_information in enumerate(row_information):
                item = QTableWidgetItem(str(col_information))
                self.ui.informationTable.setItem(i, j, item)

    def renew_the_book(self):
        # 按下续借框后续借当前书籍，根据是否成功来决定下一步操作
        current_row = self.ui.informationTable.currentRow()
        isbn = self.ui.informationTable.item(current_row, 0).text()
        # TODO: 根据ISBN与user_name进行续借相关操作
        print(isbn)

    def return_the_book(self):
        current_row = self.ui.informationTable.currentRow()
        isbn = self.ui.informationTable.item(current_row, 0).text()
        # TODO: 根据ISBN与user_name进行归还相关操作
        print(isbn)

    def jump_to_back(self):
        # 跳转到上一层
        self.back = StudentMainWindow(self.user_name)
        self.back.ui.show()
        self.ui.close()
