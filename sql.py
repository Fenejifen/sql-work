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
    cursor.execute("use `sql-work`") # 在这里输入数据库名字

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
    def search_book(cls, book_name, book_isbn, book_author, book_press, book_type, book_remainder):
        if book_type == "":
            if book_remainder:
                cls.cursor.execute(f"select * from 书籍 where ISBN like '%{book_isbn}%' and 书名 like '%{book_name}%' and 作者 like '%{book_author}%' and 出版社 like '%{book_press}%' and 可借书籍数 > 0")
            else:
                cls.cursor.execute(
                f"select * from 书籍 where ISBN like '%{book_isbn}%' and 书名 like '%{book_name}%' and 作者 like '%{book_author}%' and 出版社 like '%{book_press}%'")
        else:
            if book_remainder:
                cls.cursor.execute(
                    f"select * from 书籍 where ISBN like '%{book_isbn}%' and 书名 like '%{book_name}%' and 作者 like '%{book_author}%' and 出版社 like '%{book_press}%' and 类型 = '{book_type}' and 可借书籍数 > 0")
            else:
                cls.cursor.execute(
                    f"select * from 书籍 where ISBN like '%{book_isbn}%' and 书名 like '%{book_name}%' and 作者 like '%{book_author}%' and 出版社 like '%{book_press}%' and 类型 = '{book_type}'")
        return cls.cursor.fetchall()

    @classmethod
    def get_borrow_information(cls, user_name):
        cls.cursor.execute(
            f"select ISBN,书名,作者,借阅时间,应还时间,续借次数 from 学生借阅未归还书籍信息 where 学号 = '{user_name}'")
        return cls.cursor.fetchall()

    @classmethod
    def get_book_information(cls):
        cls.cursor.execute("select * from 书籍")
        return cls.cursor.fetchall()

    @classmethod
    def change_book_information(cls, current_row, book_information):
        # 改变图书信息，有增加与修改两种情况
        old_book_information = SQL.get_book_information()
        try:
            if current_row >= len(old_book_information):
                # 增加情况
                print(book_information)
                cls.cursor.execute(f"insert into 书籍 values("
                                   f"{book_information[0]},"
                                   f"'{book_information[1]}',"
                                   f"'{book_information[2]}',"
                                   f"'{book_information[3]}',"
                                   f"'{book_information[4]}',"
                                   f"{book_information[5]},"
                                   f"{book_information[6]})")
            else:
                # 修改情况
                old_isbn = old_book_information[current_row][0]
                cls.cursor.execute(f"update 书籍 set "
                                   f"ISBN={book_information[0]},"
                                   f"书名='{book_information[1]}',"
                                   f"作者='{book_information[2]}',"
                                   f"出版社='{book_information[3]}',"
                                   f"类型='{book_information[4]}',"
                                   f"馆藏总数={book_information[5]},"
                                   f"可借书籍数={book_information[6]} "
                                   f"where ISBN = {old_isbn}")
        except Exception as result:
            print(result)
            cls.db.rollback()
            return 1
        else:
            cls.db.commit()
            return 0

    @classmethod
    def delete_the_book(cls, current_row):
        # 删除当前行的书籍信息,成功则返回0，未知错误返回1,有请求未确认返回2，有书还没还返回3
        isbn = SQL.get_book_information()[current_row][0]
        # 有请求情况
        cls.cursor.execute(f"select * from 待确认事项 where ISBN={isbn}")
        if cls.cursor.fetchone() is not None:
            return 2
        # 未归还情况
        cls.cursor.execute(f"select * from 学生借阅未归还书籍信息 where ISBN={isbn}")
        if cls.cursor.fetchone() is not None:
            return 3
        # 删除
        try:
            cls.cursor.execute(f"delete from 书籍 where ISBN={isbn}")
        except Exception as result:
            # 出现异常情况
            print(result)
            cls.db.rollback()
            return 1
        else:
            # 正常删除情况
            cls.db.commit()
            return 0

    @classmethod
    def get_student_information(cls):
        cls.cursor.execute("select * from 学生")
        return cls.cursor.fetchall()

    @classmethod
    def delete_the_student(cls, current_row):
        # 删除当前行的学生信息,成功则返回0，未知错误返回1,有请求未确认返回2，有书还没还返回3
        user_name = SQL.get_student_information()[current_row][0]
        # 有请求情况
        cls.cursor.execute(f"select * from 待确认事项 where 学号={user_name}")
        if cls.cursor.fetchone() is not None:
            return 2
        # 未归还情况
        cls.cursor.execute(f"select * from 学生借阅未归还书籍信息 where 学号={user_name}")
        if cls.cursor.fetchone() is not None:
            return 3
        # 删除
        try:
            cls.cursor.execute(f"delete from 学生 where 学工号={user_name}")
        except Exception as result:
            # 出现异常情况
            print(result)
            cls.db.rollback()
            return 1
        else:
            # 正常删除情况
            cls.db.commit()
            return 0

    @classmethod
    def change_student_information(cls, current_row, student_information):
        # 修改学生信息，有增加与更新两种情况，正常返回0，出现异常返回1
        old_student_information = SQL.get_student_information()
        try:
            if current_row >= len(old_student_information):
                # 增加情况
                print(student_information)
                cls.cursor.execute(f"insert into 学生 values("
                                   f"{student_information[0]},"
                                   f"'{student_information[1]}',"
                                   f"'{student_information[2]}',"
                                   f"'{student_information[3]}',"
                                   f"'{student_information[4]}',"
                                   f"'{student_information[5]}',"
                                   f"{student_information[6]},"
                                   f"{student_information[7]},"
                                   f"{student_information[8]})")
            else:
                # 修改情况
                old_user_name = old_student_information[current_row][0]
                cls.cursor.execute(f"update 学生 set "
                                   f"学工号={student_information[0]},"
                                   f"姓名='{student_information[1]}',"
                                   f"年龄='{student_information[2]}',"
                                   f"班级='{student_information[3]}',"
                                   f"专业='{student_information[4]}',"
                                   f"性别='{student_information[5]}',"
                                   f"联系方式={student_information[6]},"
                                   f"账户密码={student_information[7]},"
                                   f"剩余可借阅书籍数={student_information[8]} "
                                   f"where 学工号 = {old_user_name}")
        except Exception as result:
            print(result)
            cls.db.rollback()
            return 1
        else:
            cls.db.commit()
            return 0

    @classmethod
    def get_confirm_information(cls):
        cls.cursor.execute("select * from 待确认事项")
        return cls.cursor.fetchall()

    @classmethod
    def confirm_the_confirmation(cls, confirmation_name, user_name):
        # 得到操作编号后查询操作申请表，根据不同的操作类型进行不同操作

        # 得到学号,ISBN,申请日期，操作类型等信息
        cls.cursor.execute(f"select 操作类型,学号,ISBN,申请日期 from 操作申请 where 操作编号 = {confirmation_name}")
        information = cls.cursor.fetchone()
        operation_type = information[0]
        student_user_name = information[1]
        isbn = information[2]
        date_time = information[3]

        # 开始根据不同类型进行不同操作
        if operation_type == '借阅':
            # 借阅操作，修改借阅信息表与操作申请表即可
            # 借阅信息表,加入学号，ISBN，借阅时间，续借次数为0
            cls.cursor.execute(
                f"insert into 借阅信息 (学号,ISBN,借阅时间,续借次数) values ({student_user_name},{isbn},'{date_time}',0) ")
            cls.cursor.execute('select last_insert_id()')
            borrow_id = cls.cursor.fetchone()[0]
            # 操作申请表，将本次操作的工号与是否同意，对应借阅信息表的编号进行填写
            cls.cursor.execute(
                f"update 操作申请 set 工号 = {user_name}, 是否同意='1', 借阅编号={borrow_id} where 操作编号={confirmation_name}")
        elif operation_type == '续借':
            # 续借操作，更新借阅信息表的续借次数项与操作申请表
            cls.cursor.execute(
                f"select 借阅编号 from 学生借阅未归还书籍信息 where ISBN={isbn} and 学号={student_user_name}")
            borrow_id = cls.cursor.fetchone()[0]
            # 更新借阅信息表的续借次数项目
            cls.cursor.execute(f"update 学生借阅未归还书籍信息 set 续借次数=续借次数+1 where 借阅编号={borrow_id}")
            # 操作申请表，将本次操作的工号与是否同意，对应借阅信息表的编号进行填写
            cls.cursor.execute(
                f"update 操作申请 set 工号 = {user_name}, 是否同意='1', 借阅编号={borrow_id} where 操作编号={confirmation_name}")
        elif operation_type == '归还':
            # 归还操作，更新借阅信息表的归还时间选项，更新操作申请表，学生可借阅书籍数+1，书籍数+1
            cls.cursor.execute(
                f"select 借阅编号 from 学生借阅未归还书籍信息 where ISBN={isbn} and 学号={student_user_name}")
            borrow_id = cls.cursor.fetchone()[0]
            # 更新借阅信息表的归还时间项目
            cls.cursor.execute(f"update 借阅信息 set 归还时间='{date_time}' where 借阅编号={borrow_id}")
            # 操作申请表，将本次操作的工号与是否同意，对应借阅信息表的编号进行填写
            cls.cursor.execute(
                f"update 操作申请 set 工号 = {user_name}, 是否同意='1', 借阅编号={borrow_id} where 操作编号={confirmation_name}")
            # 更新可借阅书籍数和书籍数
            cls.cursor.execute(
                f"update 学生 set 剩余可借阅书籍数 = 剩余可借阅书籍数 + 1 where 学工号 = {student_user_name}")
            cls.cursor.execute(f"update 书籍 set 可借书籍数 = 可借书籍数 + 1 where ISBN = {isbn}")
        cls.db.commit()

    @classmethod
    def reject_the_confirmation(cls, confirmation_name, user_name, reject_reason):
        # 所有拒绝操作都需要在操作申请表中填写工号、是否同意与备注
        cls.cursor.execute(
            f"update 操作申请 set 工号={user_name},是否同意=0,备注='{reject_reason}' where 操作编号 = {confirmation_name}")
        # 之后根据拒绝操作类型的不同来进行不同的操作
        cls.cursor.execute(f"select 操作类型,学号,ISBN from 操作申请 where 操作编号 = {confirmation_name}")
        information = cls.cursor.fetchone()
        if information[0] == '借阅':
            # 拒绝借阅操作还需要将学生的可借阅书籍+1，图书的可借阅数+1
            cls.cursor.execute(
                f'update 学生 set 剩余可借阅书籍数 = 剩余可借阅书籍数 + 1 where 学工号 = {information[1]}')
            cls.cursor.execute(f'update 书籍 set 可借书籍数 = 可借书籍数 + 1 where ISBN = {information[2]}')
        elif information[0] == '续借':
            # 拒绝续借操作只需要完善操作申请表即可
            pass
        elif information[0] == '归还':
            # 拒绝归还操作只需要完善操作申请表即可
            pass
        cls.db.commit()

    @classmethod
    def borrow_the_book(cls, isbn, user_name):
        # 让学号为user_name的学生预订借阅当前ISBN的书籍，返回码0表示借阅成功，1表示没有图书，2表示超出借阅上限,3表示正在借阅,4表示重复申请
        # 判断是否有剩余图书
        cls.cursor.execute(f"select 可借书籍数 from 书籍 where ISBN = {isbn} ")
        if cls.cursor.fetchone()[0] == 0:
            return 1
        # 判断是否达到借阅上限
        cls.cursor.execute(f"select 剩余可借阅书籍数 from 学生 where 学工号 = {user_name}")
        if cls.cursor.fetchone()[0] == 0:
            return 2
        # 判断是否该学生已经借阅过本书
        cls.cursor.execute(
            f"select 借阅编号 from 借阅信息 where 学号 = {user_name} and ISBN={isbn} and 归还时间 is NULL")
        if cls.cursor.fetchone() is not None:
            return 3
        # 判断学生是否重复申请
        cls.cursor.execute(f"select 操作编号 from 操作申请 where 是否同意 is NULL and 学号={user_name} and ISBN={isbn}")
        if cls.cursor.fetchone() is not None:
            return 4
        # 进行操作申请操作，包括书籍-1，可借阅书籍-1，操作申请表中增加数据内容
        cls.cursor.execute(f"update 书籍 set 可借书籍数 = 可借书籍数 - 1 where ISBN = {isbn}")
        cls.cursor.execute(f"update 学生 set 剩余可借阅书籍数 = 剩余可借阅书籍数 - 1 where 学工号 = {user_name}")
        cls.cursor.execute(f"insert into 操作申请 (学号,ISBN, 申请日期, 操作类型) values ({user_name}, "
                           f"{isbn},'{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}', '借阅')")
        cls.db.commit()
        return 0

    @classmethod
    def renew_the_book(cls, isbn, user_name):
        # 让学号为user_name的学生续借当前ISBN的书籍，返回码0表示续借申请成功，1表示已经续借过了,2表示已经申请过了
        # 判断是否已经续借过
        cls.cursor.execute(f"select 续借次数 from 借阅信息 where 学号={user_name} and ISBN={isbn} and 归还时间 is null")
        if cls.cursor.fetchone()[0] != 0:
            return 1
        # 判断是否重复申请
        cls.cursor.execute(f"select 操作类型 from 操作申请 where 是否同意 is NULL and 学号={user_name} and ISBN={isbn}")
        information = cls.cursor.fetchone()
        if information is not None:
            operation_type = information[0]
            if operation_type == '续借':
                return 2
            elif operation_type == '归还':
                return 3
        # 进行操作申请操作，只需要在操作申请表中插入信息即可
        cls.cursor.execute(f"insert into 操作申请 (学号,ISBN,申请日期,操作类型) values ({user_name}, {isbn}, "
                           f"'{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}', '续借')")
        cls.db.commit()

        return 0

    @classmethod
    def return_the_book(cls, isbn, user_name):
        # 让学号为user_name的学生归还当前ISBN的书籍，返回码0表示归还申请成功，1表示已经申请归还，2表示已申请续借
        # 判断是否重复申请
        cls.cursor.execute(f"select 操作类型 from 操作申请 where 是否同意 is NULL and 学号={user_name} and ISBN={isbn}")
        information = cls.cursor.fetchone()
        if information is not None:
            operation_type = information[0]
            if operation_type == '归还':
                return 1
            elif operation_type == '续借':
                return 2
        # 进行操作申请操作，只需要在操作申请表中插入信息即可
        cls.cursor.execute(f"insert into 操作申请 (学号,ISBN,申请日期,操作类型) values ({user_name}, {isbn}, "
                           f"'{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}', '归还')")
        cls.db.commit()

        return 0

    @classmethod
    def search_student(cls, student_name, student_user_name, student_class, student_major, student_sex):
        cls.cursor.execute(f"select * from 学生 where 姓名 like '%{student_name}%' and 学工号 like '%{student_user_name}%' and 班级 like '%{student_class}%' and 专业 like '%{student_major}%' and 性别 like '%{student_sex}%'")
        return cls.cursor.fetchall()

    @classmethod
    def get_book_types(cls):
        cls.cursor.execute("select distinct 类型 from 书籍")
        return cls.cursor.fetchall()

    @classmethod
    def get_class_types(cls):
        cls.cursor.execute("select distinct 班级 from 学生")
        return cls.cursor.fetchall()

    @classmethod
    def get_major_types(cls):
        cls.cursor.execute("select distinct 专业 from 学生")
        return cls.cursor.fetchall()
