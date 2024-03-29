"""
存储所有关于登录窗口相关的类
"""

from PySide2.QtGui import QImage, QPixmap, QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMessageBox, QGraphicsScene, QGraphicsPixmapItem, QTableWidgetItem, QInputDialog, \
    QLineEdit

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
        self.renewAndReturn = RenewAndReturn(self.user_name)
        self.renewAndReturn.ui.show()
        self.ui.close()

    def jump_to_queryAndBorrow(self):
        self.queryAndBorrow = QueryAndBorrowWindow(self.user_name)
        self.queryAndBorrow.ui.show()
        self.ui.close()

    def get_personal_data(self):
        # 得到个人信息，显示在学生操作界面右上角
        information = SQL.get_students_personal_data(self.user_name, True)
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
        self.ui.bookManagement.clicked.connect(self.jump_to_bookManagement)
        self.ui.studentManagement.clicked.connect(self.jump_to_studentManagement)
        self.ui.confirmationManagement.clicked.connect(self.jump_to_confirmationManagement)
        self.ui.backButton.clicked.connect(self.jump_to_back)

    def jump_to_confirmationManagement(self):
        self.confirmationManagement = ConfirmationManagement(self.user_name)
        self.confirmationManagement.ui.show()
        self.ui.close()

    def jump_to_studentManagement(self):
        self.studentManagement = StudentManagement(self.user_name)
        self.studentManagement.ui.show()
        self.ui.close()

    def jump_to_bookManagement(self):
        self.bookManagement = BookManagement(self.user_name)
        self.bookManagement.ui.show()
        self.ui.close()

    def jump_to_back(self):
        # 跳转到上一层
        self.back = AdminLoginWindow()
        self.back.ui.show()
        self.ui.close()

    def get_personal_data(self):
        # 得到个人信息，显示在学生操作界面右上角
        information = SQL.get_students_personal_data(self.user_name, False)
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


class QueryAndBorrowWindow:
    """
    查询与借阅界面
    """

    def __init__(self, user_name):
        self.ui = QUiLoader().load('./ui/queryAndBorrow.ui')
        self.user_name = user_name

        # 获取界面相关信息
        self.search_book()

        # 设置搜索框图标
        self.ui.searchButton.setIcon(QIcon('ui/search.jpeg'))

        # 绑定操作按钮
        self.ui.searchButton.clicked.connect(self.search_book)
        self.ui.borrowButton.clicked.connect(self.borrow_the_book)
        self.ui.backButton.clicked.connect(self.jump_to_back)
        self.ui.advancedSearchButton.clicked.connect(self.show_advanced_search)

        # 设置隐藏高级搜索选项
        self.hide_advanced_search()

    def show_advanced_search(self):
        # 显示各项目
        self.ui.widget.show()

        # 搜索并添加书籍类型
        self.ui.typeBox.clear()
        self.ui.typeBox.addItem('')
        book_types = SQL.get_book_types()
        for book_type in book_types:
            self.ui.typeBox.addItem(book_type[0])

        # 再次按下隐藏
        self.ui.advancedSearchButton.clicked.connect(self.hide_advanced_search)

    def hide_advanced_search(self):
        # 隐藏各项目
        self.ui.widget.hide()
        self.ui.typeBox.clear()
        # 再次按下显示
        self.ui.advancedSearchButton.clicked.connect(self.show_advanced_search)

    def borrow_the_book(self):
        # 按下借阅框后借阅当前选中行的书籍,并视是否借阅成功而执行各种操作
        current_row = self.ui.informationTable.currentRow()
        isbn = self.ui.informationTable.item(current_row, 0).text()
        exit_code = SQL.borrow_the_book(isbn, self.user_name)
        if exit_code == 0:
            QMessageBox.about(self.ui, '操作成功', '书籍已预订请寻找管理员进行确定操作')
            print("借阅成功")
        elif exit_code == 1:
            QMessageBox.critical(self.ui, '操作失败', '书籍被借阅光了')
        elif exit_code == 2:
            QMessageBox.critical(self.ui, '操作失败', '您当前借阅书籍数量已达上限')
        elif exit_code == 3:
            QMessageBox.critical(self.ui, '操作失败', '您已经借阅了当前书籍')
        elif exit_code == 4:
            QMessageBox.critical(self.ui, '操作失败', '您已申请了借阅当前书籍')
        # 刷新界面
        self.ui.informationTable.setRowCount(0)
        self.search_book()

    def search_book(self):
        # 按下搜索按钮后获取全部信息并搜索输出至信息框
        book_name = self.ui.bookNameEdit.text()
        book_isbn = self.ui.ISBNEdit.text()
        book_author = self.ui.authorEdit.text()
        book_press = self.ui.pressEdit.text()
        book_type = self.ui.typeBox.currentText()
        book_remainder = self.ui.remainderButton.isChecked()
        book_information = SQL.search_book(book_name,book_isbn,book_author,book_press,book_type,book_remainder)
        # 测试代码
        print("搜索的图书信息:",book_name, book_isbn, book_author, book_press, book_type, book_remainder)
        self.ui.informationTable.setRowCount(0)
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


class RenewAndReturn:
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
        exit_code = SQL.renew_the_book(isbn, self.user_name)
        if exit_code == 0:
            QMessageBox.about(self.ui, '操作成功', '书籍已续借请寻找管理员进行确定操作')
        elif exit_code == 1:
            QMessageBox.critical(self.ui, '操作失败', '您已经续借过这本书了')
        elif exit_code == 2:
            QMessageBox.critical(self.ui, '操作失败', '请勿重复申请')
        elif exit_code == 3:
            QMessageBox.critical(self.ui, '操作失败', '已经有归还申请了')
        print(isbn)

    def return_the_book(self):
        current_row = self.ui.informationTable.currentRow()
        isbn = self.ui.informationTable.item(current_row, 0).text()
        exit_code = SQL.return_the_book(isbn, self.user_name)
        if exit_code == 0:
            QMessageBox.about(self.ui, '操作成功', '书籍已申请归还请寻找管理员进行确定操作')
        elif exit_code == 1:
            QMessageBox.critical(self.ui, '操作失败', '请勿重复申请')
        elif exit_code == 2:
            QMessageBox.critical(self.ui, '操作失败', '已经有续借申请了')

    def jump_to_back(self):
        # 跳转到上一层
        self.back = StudentMainWindow(self.user_name)
        self.back.ui.show()
        self.ui.close()


class BookManagement:
    """
    管理员进行图书管理的界面
    """

    def __init__(self, user_name):
        self.ui = QUiLoader().load('./ui/bookManagement.ui')
        self.user_name = user_name

        # 获取界面相关信息
        self.search_book()

        # 设置搜索框图标
        self.ui.searchButton.setIcon(QIcon('ui/search.jpeg'))

        # 绑定操作按钮
        self.ui.searchButton.clicked.connect(self.search_book)
        self.ui.addBookButton.clicked.connect(self.add_book)
        self.ui.deleteBookButton.clicked.connect(self.delete_the_book)
        self.ui.submitButton.clicked.connect(self.submit_the_book)
        self.ui.backButton.clicked.connect(self.jump_to_back)
        self.ui.advancedSearchButton.clicked.connect(self.show_advanced_search)

        # 设置隐藏高级搜索选项
        self.hide_advanced_search()

    def show_advanced_search(self):
        # 显示各项目
        self.ui.widget.show()

        # 搜索并添加书籍类型
        self.ui.typeBox.clear()
        self.ui.typeBox.addItem('')
        book_types = SQL.get_book_types()
        for book_type in book_types:
            self.ui.typeBox.addItem(book_type[0])

        # 再次按下隐藏
        self.ui.advancedSearchButton.clicked.connect(self.hide_advanced_search)

    def hide_advanced_search(self):
        # 隐藏各项目
        self.ui.widget.hide()
        self.ui.typeBox.clear()
        # 再次按下显示
        self.ui.advancedSearchButton.clicked.connect(self.show_advanced_search)
    def search_book(self):
        # 按下搜索按钮后获取全部信息并搜索输出至信息框
        book_name = self.ui.bookNameEdit.text()
        book_isbn = self.ui.ISBNEdit.text()
        book_author = self.ui.authorEdit.text()
        book_press = self.ui.pressEdit.text()
        book_type = self.ui.typeBox.currentText()
        book_remainder = self.ui.remainderButton.isChecked()
        book_information = SQL.search_book(book_name,book_isbn,book_author,book_press,book_type,book_remainder)
        # 测试代码
        print("搜索的图书信息:",book_name, book_isbn, book_author, book_press, book_type, book_remainder)
        self.ui.informationTable.setRowCount(0)
        self.ui.searchInformationLabel.setText(f"共搜索到了{len(book_information)}个结果")
        self.ui.informationTable.clearContents()
        for i, row_information in enumerate(book_information):
            self.ui.informationTable.insertRow(i)
            for j, col_information in enumerate(row_information):
                item = QTableWidgetItem(str(col_information))
                self.ui.informationTable.setItem(i, j, item)

    def submit_the_book(self):
        current_row = self.ui.informationTable.currentRow()
        book_information = [
            self.ui.informationTable.item(current_row, 0).text(),
            self.ui.informationTable.item(current_row, 1).text(),
            self.ui.informationTable.item(current_row, 2).text(),
            self.ui.informationTable.item(current_row, 3).text(),
            self.ui.informationTable.item(current_row, 4).text(),
            self.ui.informationTable.item(current_row, 5).text(),
            self.ui.informationTable.item(current_row, 6).text()]
        exit_code = SQL.change_book_information(current_row,book_information)
        if exit_code == 0:
            QMessageBox.information(
                self.ui,
                '操作成功',
                '成功修改')
            self.ui.informationTable.setRowCount(0)
            self.search_book()
        if exit_code == 1:
            QMessageBox.critical(self.ui, '操作失败', '出现异常错误')


    def add_book(self):
        self.ui.informationTable.setRowCount(0)
        self.search_book()
        row_count = self.ui.informationTable.rowCount()
        self.ui.informationTable.insertRow(row_count)

    def delete_the_book(self):
        # 删除当前选中行的书籍，会弹出选项框确定，会根据是否删除成功而返回不同的值
        current_row = self.ui.informationTable.currentRow()
        choice = QMessageBox.question(
            self.ui,
            '确认删除',
            '确认要删除本书籍吗?'
        )
        if choice == QMessageBox.Yes:
            exit_code = SQL.delete_the_book(current_row)
            self.ui.informationTable.setRowCount(0)
            self.search_book()
            if exit_code == 0:
                QMessageBox.information(
                    self.ui,
                    '操作成功',
                    '成功修改')
            if exit_code == 1:
                QMessageBox.critical(self.ui, '操作失败', '出现异常错误')
            if exit_code == 2:
                QMessageBox.critical(self.ui, '操作失败', '本书仍有请求未处理')
            if exit_code == 3:
                QMessageBox.critical(self.ui, '操作失败', '本书未被归还')
        # 刷新界面
        self.ui.informationTable.setRowCount(0)
        self.search_book()

    def jump_to_back(self):
        # 跳转到上一层
        self.back = AdminMainWindow(self.user_name)
        self.back.ui.show()
        self.ui.close()

class StudentManagement:
    """
    管理员进行学生管理的界面
    """

    def __init__(self, user_name):
        self.ui = QUiLoader().load('./ui/studentManagement.ui')
        self.user_name = user_name

        # 获取界面相关信息
        self.search_student()

        # 设置搜索框图标
        self.ui.searchButton.setIcon(QIcon('ui/search.jpeg'))

        # 绑定操作按钮
        self.ui.searchButton.clicked.connect(self.search_student)
        self.ui.addStudentButton.clicked.connect(self.add_student)
        self.ui.deleteStudentButton.clicked.connect(self.delete_the_student)
        self.ui.submitButton.clicked.connect(self.submit_the_student)
        self.ui.backButton.clicked.connect(self.jump_to_back)
        self.ui.advancedSearchButton.clicked.connect(self.show_advanced_search)

        # 设置隐藏高级搜索选项
        self.hide_advanced_search()

    def show_advanced_search(self):
        # 显示各项目
        self.ui.widget.show()

        # 搜索并添加班级类型
        self.ui.classBox.clear()
        self.ui.classBox.addItem('')
        class_types = SQL.get_class_types()
        for class_type in class_types:
            self.ui.classBox.addItem(class_type[0])

        # 搜索并添加专业类型
        self.ui.majorBox.clear()
        self.ui.majorBox.addItem('')
        major_types = SQL.get_major_types()
        for major_type in major_types:
            self.ui.majorBox.addItem(major_type[0])

        # 再次按下隐藏
        self.ui.advancedSearchButton.clicked.connect(self.hide_advanced_search)

    def hide_advanced_search(self):
        # 隐藏各项目
        self.ui.widget.hide()
        self.ui.classBox.clear()
        self.ui.majorBox.clear()
        # 再次按下显示
        self.ui.advancedSearchButton.clicked.connect(self.show_advanced_search)

    def submit_the_student(self):
        current_row = self.ui.informationTable.currentRow()
        student_information = [
            self.ui.informationTable.item(current_row, 0).text(),
            self.ui.informationTable.item(current_row, 1).text(),
            self.ui.informationTable.item(current_row, 2).text(),
            self.ui.informationTable.item(current_row, 3).text(),
            self.ui.informationTable.item(current_row, 4).text(),
            self.ui.informationTable.item(current_row, 5).text(),
            self.ui.informationTable.item(current_row, 6).text(),
            self.ui.informationTable.item(current_row, 7).text(),
            self.ui.informationTable.item(current_row, 8).text()
        ]
        exit_code = SQL.change_student_information(current_row,student_information)
        if exit_code == 0:
            QMessageBox.information(
                self.ui,
                '操作成功',
                '成功修改')
        if exit_code == 1:
            QMessageBox.critical(self.ui, '操作失败', '出现异常错误')
        # 刷新界面
        self.ui.informationTable.setRowCount(0)
        self.search_student()

    def add_student(self):
        row_count = self.ui.informationTable.rowCount()
        self.ui.informationTable.insertRow(row_count)

    def delete_the_student(self):
        # 删除当前选中行的书籍，会弹出选项框确定，会根据是否删除成功而返回不同的值
        current_row = self.ui.informationTable.currentRow()
        choice = QMessageBox.question(
            self.ui,
            '确认删除',
            '确认要删除该学生信息吗?'
        )
        if choice == QMessageBox.Yes:
            exit_code = SQL.delete_the_student(current_row)
            if exit_code == 0:
                QMessageBox.information(
                    self.ui,
                    '操作成功',
                    '成功删除学生信息')
            if exit_code == 1:
                QMessageBox.critical(self.ui, '操作失败', '出现异常错误')
            if exit_code == 2:
                QMessageBox.critical(self.ui, '操作失败', '该学生仍有请求未处理')
            if exit_code == 3:
                QMessageBox.critical(self.ui, '操作失败', '该学生有书未被归还')
        # 刷新界面
        self.ui.informationTable.setRowCount(0)
        self.search_student()

    def search_student(self):
        # 按下搜索按钮后获取全部信息并搜索输出至信息框
        student_name = self.ui.studentNameEdit.text()
        student_user_name = self.ui.userNameEdit.text()
        student_class = self.ui.classBox.currentText()
        student_major = self.ui.majorBox.currentText()
        student_sex = self.ui.sexBox.currentText()
        student_information = SQL.search_student(student_name,student_user_name,student_class,student_major,student_sex)
        # 测试代码
        print("搜索的学生信息:",student_name, student_user_name, student_class, student_major, student_sex)
        self.ui.informationTable.setRowCount(0)
        self.ui.searchInformationLabel.setText(f"共搜索到了{len(student_information)}个结果")
        self.ui.informationTable.clearContents()
        for i, row_information in enumerate(student_information):
            self.ui.informationTable.insertRow(i)
            for j, col_information in enumerate(row_information):
                item = QTableWidgetItem(str(col_information))
                self.ui.informationTable.setItem(i, j, item)

    def jump_to_back(self):
        # 跳转到上一层
        self.back = AdminMainWindow(self.user_name)
        self.back.ui.show()
        self.ui.close()

class ConfirmationManagement:
    # TODO: 加入待确认事项搜索框
    def __init__(self, user_name):
        self.ui = QUiLoader().load('./ui/confirmationManagement.ui')
        self.user_name = user_name;
        # 获取界面相关信息
        self.get_confirm_information()

        # 绑定操作按钮
        self.ui.confirmButton.clicked.connect(self.confirm_the_confirmation)
        self.ui.rejectButton.clicked.connect(self.reject_the_confirmation)
        self.ui.backButton.clicked.connect(self.jump_to_back)

    def confirm_the_confirmation(self):
        # 接受当前选中行的请求，会弹出选项框确定，会根据是否删除成功而返回不同的值
        current_row = self.ui.informationTable.currentRow()
        choice = QMessageBox.question(
            self.ui,
            '确认接受',
            '确认要接受该请求吗?'
        )
        if choice == QMessageBox.Yes:
            confirmation_name = self.ui.informationTable.item(current_row, 0).text()
            SQL.confirm_the_confirmation(confirmation_name, self.user_name)
            self.ui.informationTable.setRowCount(0)
            self.get_confirm_information()
            QMessageBox.information(
                self.ui,
                '操作成功',
                '成功接受该请求')
        else:
            QMessageBox.information(
                self.ui,
                '操作取消',
                '您取消了接受操作')

    def reject_the_confirmation(self):
        #拒绝当前选中行的请求，会弹出选项框确定，会根据是否删除成功而返回不同的值
        current_row = self.ui.informationTable.currentRow()
        reject_reason, okPressed = QInputDialog.getText(
            self.ui,
            "拒绝请求",
            "请输入拒绝原因:",
            QLineEdit.Normal,
            "")
        if okPressed:
            confirmation_name = self.ui.informationTable.item(current_row, 0).text()
            SQL.reject_the_confirmation(confirmation_name, self.user_name, reject_reason)
            self.ui.informationTable.setRowCount(0)
            self.get_confirm_information()
            QMessageBox.information(
                self.ui,
                '操作成功',
                '成功拒绝该请求')
        else:
            QMessageBox.information(
                self.ui,
                '操作取消',
                '您取消了拒绝操作')

    def get_confirm_information(self):
        confirm_information = SQL.get_confirm_information()
        self.ui.confirmationInformationLabel.setText(f"当前共有{len(confirm_information)}个待处理事项")
        for i, row_information in enumerate(confirm_information):
            self.ui.informationTable.insertRow(i)
            for j, col_information in enumerate(row_information):
                item = QTableWidgetItem(str(col_information))
                self.ui.informationTable.setItem(i, j, item)

    def jump_to_back(self):
        # 跳转到上一层
        self.back = AdminMainWindow(self.user_name)
        self.back.ui.show()
        self.ui.close()
