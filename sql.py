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

        # TODO:删除调试代码
        print(account_information_dict)
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
