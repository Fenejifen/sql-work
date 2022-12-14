import pymysql


class SQL:
    """
    控制数据库的类，包含了所有需要数据库的函数
    只是为了代码方便才设计成这样，全部使用类函数
    """
    db = pymysql.connect(
        host="localhost",
        port=3306,
        user='root',  # 在这里输入用户名
        password='',  # 在这里输入密码
        charset='utf8mb4'
    )  # 连接数据库
    cursor = db.cursor()
    cursor.execute("use `sql-work`")

    @classmethod
    def check_login(cls, user_name, pass_word, is_student):
        """
        检查用户名与密码是否正确，正确则返回True，否则返回False
        """
        # 判断账户信息的视图
        if is_student:
            view_name = '学生账号密码'
        else:
            view_name = '管理员账号密码'

        # 获取账户密码数据并判断
        cls.cursor.execute(f"select * from {view_name}")
        account_information_tuple = cls.cursor.fetchall()
        account_information_dict = {}

        # 得到的账户信息为元组，为了方便判断转化为字典
        for account_information in account_information_tuple:
            account_information_dict.setdefault(account_information[0], account_information[1])

        if user_name in account_information_dict and pass_word == account_information_dict[user_name]:
            print("登录成功")
            return True
        else:
            print("登录失败,账号或密码错误")
            return False

    @classmethod
    def get_students_personal_data(cls, user_name, is_student):
        """
        获取学生个人信息，返回一个元组
        """
        if is_student:
            view_name = '学生平台个人展示信息'
        else:
            view_name = '管理员平台个人展示信息'
        cls.cursor.execute(f"select * from {view_name} where 学工号 = {user_name}")
        return cls.cursor.fetchone()

    @classmethod
    def search_book_by_name(cls, book_name):
        # TODO:加入借阅信息中关于最近应还书籍日期的信息
        cls.cursor.execute(f"select * from 学生查询书籍信息 where 书名 like '%{book_name}%' ")
        return cls.cursor.fetchall()

    @classmethod
    def get_borrow_information(cls, user_name):
        cls.cursor.execute(
            f"select ISBN,书名,作者,借阅时间,应还时间,续借次数 from 学生借阅书籍信息 where 学号 = '{user_name}'")
        return cls.cursor.fetchall()

    @classmethod
    def get_book_information(cls):
        cls.cursor.execute("select * from 书籍")
        return cls.cursor.fetchall()

    @classmethod
    def change_book_information(cls, book_information):
        # TODO:根据book_information进行修改书籍相关信息，并返回True或False
        pass

    @classmethod
    def delete_the_book(cls, isbn):
        # TODO:删除isbn书籍，并且返回True或False
        pass

    @classmethod
    def get_student_information(cls):
        cls.cursor.execute("select * from 学生")
        return cls.cursor.fetchall()

    @classmethod
    def delete_the_student(cls, student_user_name):
        # TODO:删除isbn书籍，并且返回True或False
        pass

    @classmethod
    def change_student_information(cls, student_information):
        # TODO:根据book_information进行修改书籍相关信息，并返回True或False
        pass

    @classmethod
    def get_confirm_information(cls):
        cls.cursor.execute("select * from 待确认事项")
        return cls.cursor.fetchall()

    @classmethod
    def confirm_the_confirmation(cls, confirmation_name):
        # TODO:根据confirmation_name进行相关确认操作，并返回True或False
        pass

    @classmethod
    def reject_the_confirmation(cls, confirmation_name):
        # TODO:根据confirmation_name进行相关拒绝操作，并返回True或False
        pass