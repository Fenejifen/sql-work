import time

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
    def confirm_the_confirmation(cls, confirmation_name, user_name):
        # 得到操作编号后查询操作申请表，根据不同的操作类型进行不同操作
        # 得到学号,ISBN,申请日期，操作类型信息
        cls.cursor.execute(f"select 操作类型,学号,ISBN,申请日期 from 操作申请 where 操作编号 = {confirmation_name}")
        information = cls.cursor.fetchone()
        if information[0] == '借阅':
            # 借阅操作，修改借阅信息表与操作申请表即可
            # 借阅信息表,加入学号，ISBN，借阅时间，续借次数为0
            cls.cursor.execute(
                f"insert into 借阅信息 (学号,ISBN,借阅时间,续借次数) values ({information[1]},{information[2]},'{information[3]}',0) ")
            cls.cursor.execute('select last_insert_id()')
            borrow_id = cls.cursor.fetchone()[0]
            # 操作申请表，将本次操作的工号与是否同意，对应借阅信息表的编号进行填写
            cls.cursor.execute(
                f"update 操作申请 set 工号 = {user_name}, 是否同意='1', 借阅编号={borrow_id} where 操作编号={confirmation_name}")
            cls.db.commit()
        elif information[0] == '续借':
            # TODO:续借与归还
            pass
        elif information[0] == '归还':
            pass

    @classmethod
    def reject_the_confirmation(cls, confirmation_name, user_name, reject_reason):
        # TODO:根据confirmation_name进行相关拒绝操作,还剩续借与归还
        # 所有拒绝操作都需要在操作申请表中填写工号、是否同意与备注
        cls.cursor.execute(f"update 操作申请 set 工号={user_name},是否同意=0,备注='{reject_reason}' where 操作编号 = {confirmation_name}")
        # 之后根据拒绝操作类型的不同来进行不同的操作
        cls.cursor.execute(f"select 操作类型,学号,ISBN from 操作申请 where 操作编号 = {confirmation_name}")
        information = cls.cursor.fetchone()
        if information[0] == '借阅':
            # 拒绝借阅操作还需要将学生的可借阅书籍+1，图书的可借阅数+1
            cls.cursor.execute(f'update 学生 set 剩余可借阅书籍数 = 剩余可借阅书籍数 + 1 where 学工号 = {information[1]}')
            cls.cursor.execute(f'update 书籍 set 可借书籍数 = 可借书籍数 + 1 where ISBN = {information[2]}')
        elif information[0] == '续借':
            pass
        elif information[0] == '归还':
            pass
        cls.db.commit()

    @classmethod
    def borrow_the_book(cls, isbn, user_name):
        # 让学号为user_name的学生预订借阅当前ISBN的书籍，返回码0表示借阅成功，1表示没有图书，2表示超出借阅上限
        # 判断是否有剩余图书
        cls.cursor.execute(f"select 可借书籍数 from 书籍 where ISBN = {isbn} ")
        if cls.cursor.fetchone()[0] == 0:
            return 1
        # 判断是否达到借阅上限
        cls.cursor.execute(f"select 剩余可借阅书籍数 from 学生 where 学工号 = {user_name}")
        if cls.cursor.fetchone()[0] == 0:
            return 2
        # 进行操作申请操作，包括书籍-1，可借阅书籍-1，操作申请表中增加数据内容
        cls.cursor.execute(f"update 书籍 set 可借书籍数 = 可借书籍数 - 1 where ISBN = {isbn}")
        cls.cursor.execute(f"update 学生 set 剩余可借阅书籍数 = 剩余可借阅书籍数 - 1 where 学工号 = {user_name}")
        cls.cursor.execute(f"insert into 操作申请 (学号,工号,ISBN, 申请日期, 操作类型) values ({user_name}, NULL, "
                           f"{isbn},'{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}', '借阅')")
        cls.db.commit()
        return 0
