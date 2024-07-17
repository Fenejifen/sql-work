# 数据库实验大作业
[![wakatime](https://wakatime.com/badge/user/aead9299-620d-4d9e-a115-cf8aa5ad290f/project/5035075f-0fb8-40f2-bc57-dc0126905c0e.svg)](https://wakatime.com/badge/user/aead9299-620d-4d9e-a115-cf8aa5ad290f/project/5035075f-0fb8-40f2-bc57-dc0126905c0e)

## 创建环境与运行程序

**首先请打开`sql.py`并修改`11-17`行代码为自己的mysql用户名与密码(非常重要)**

```bash
# 创建数据库并导入数据
> mysql
mysql> create DATABASE `sql-work`;
mysql> exit
> mysql -h localhost -u root -p sql-work < .\sql-work.sql

# 创建python环境
conda create -n sql-work python=3.8.1 # python版本请在3.8.1之上，否则可能会出现异常错误
conda activate sql-work
pip install pymysql pyside2 # 主要是安装这两个包

# 运行
python.\main.py # 运行时请确保此时在sql-work目录下，否则无法读取UI进而导致无法运行
```

虚拟环境的配置可以参考这篇博客：
[三种Anaconda虚拟环境创建方式和第三方包的安装_anaconda创建一个新的环境安装第三方库之前的第三方库可以用吗-CSDN博客](https://blog.csdn.net/weixin_40964777/article/details/117700161?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522169859072016800215072519%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=169859072016800215072519&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_ecpm_v1~rank_v31_ecpm-1-117700161-null-null.nonecase&utm_term=%E6%80%8E%E4%B9%88%E5%9C%A8anaconda%E8%99%9A%E6%8B%9F%E7%8E%AF%E5%A2%83%E4%B8%AD%E4%B8%8B%E8%BD%BD%E7%AC%AC%E4%B8%89%E6%96%B9%E5%BA%93&spm=1018.2226.3001.4450)

用命令提示符复制mysql库可以参考以下两篇博客：
1.[MySQL+MySQLWorkBench安装和配置_mysql和mysqlworkbench都要下载吗-CSDN博客](https://blog.csdn.net/xuiiao/article/details/129297574?ops_request_misc=&request_id=&biz_id=102&utm_term=%E6%80%8E%E4%B9%88%E4%B8%8B%E8%BD%BDmysql%E5%92%8Cmysqlworkbench&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~sobaiduweb~default-0-129297574.nonecase&spm=1018.2226.3001.4450)
2.[ERROR 1064 (42000): You have an error in your SQL syntax; - 知乎](https://zhuanlan.zhihu.com/p/476698808)

## 操作方法

执行命令后首先会看到一个选择是学生还是管理员登录的界面，分别对应学生与管理员的相关功能。

![image-20221216190953322](README.assets/image-20221216190953322.png)

首先进入学生登录入口，然后输入测试用学生号`2020302888`与密码`123456`，点击登录后进入学生操作界面。

![image-20221216191007140](README.assets/image-20221216191007140.png)

![image-20221216191015788](README.assets/image-20221216191015788.png)

在学生操作界面可以查看学生当前基本信息与剩余可借阅书籍数。并在下面两个按钮分别进入查询与借阅书籍，续借与归还书籍功能界面。首先来看查询与借阅功能。

![image-20221216191109376](README.assets/image-20221216191109376.png)

在当前页面下可在上方输入想要搜索的书籍名，然后点击右边搜索按钮，便会显示相关图书信息。之后选中想要借阅的书籍所在行的任意一个单元格，点击右侧借阅按钮即可发送借阅请求。之后可进入管理员界面进行申请确定。

![image-20221216191338414](README.assets/image-20221216191338414.png)

再看续借与归还功能界面，在这里会自动显示当前用户已经借阅但是未归还的书籍，在这里可以进行书籍的续借与归还，同样选中想要续借与归还的书籍行的任意一个单元格再点击右边按钮即可。

![image-20221216191527615](README.assets/image-20221216191527615.png)

![image-20221216191638211](README.assets/image-20221216191638211.png)

之后来看管理员界面，进入管理员登录入口后可输入测试用管理员账号`2020302888`与密码`123456`，点击登录后进入管理员操作界面。

![image-20221216191739728](README.assets/image-20221216191739728.png)

![image-20221216191752810](README.assets/image-20221216191752810.png)

在这里可以进行书籍管理、学生管理与待确认事项管理。先来看待确认事项管理

![image-20221216192003623](README.assets/image-20221216192003623.png)

点击按钮后来到事项管理界面，在这里会自动显示有哪些待处理事项与其操作类型，同样选中想要处理的事项所在行任意一个单元格点击确认或拒绝即可完成事项管理。

![image-20221216192138413](README.assets/image-20221216192138413.png)

之后来看书籍管理功能界面

![image-20221216192242428](README.assets/image-20221216192242428.png)

若要修改书籍信息，可以直接双击单元格然后进行修改内容，之后点击右侧提交修改按钮即可修改书籍信息，注意此时必须选中修改书籍当前行的任意一个单元格，否则无法定位是要修改哪一行书籍信息。

![image-20221216192355475](README.assets/image-20221216192355475.png)

若要进行书籍的增加，可点击右侧增加按钮，然后在多出来的新一行中输入新添加的书籍信息，输入完毕后同样选中当前行任意一个单元格点击提交修改，即可成功提交新增的书籍信息。

![image-20221216192509950](README.assets/image-20221216192509950.png)

若要进行书籍信息的删除，选中需要删除的书籍行任意一个单元格，点击右侧删除按钮并确认即可进行信息删除，删除后相关表内容中的ISBN会置为NULL。并且进行删除操作时会自动检测是否满足删除条件，如不满足则会输出相关错误信息

![image-20221216192719327](README.assets/image-20221216192719327.png)

![image-20221216192745313](README.assets/image-20221216192745313.png)

学生管理界面与操作方式与书籍管理相同，在此不做演示。

## 一些细节

photo目录下存放每个人的个人文件图标，命名为`学工号.jpg`即可显示
