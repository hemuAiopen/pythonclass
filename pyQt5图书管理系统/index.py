# 14:30 PyQt5 图书管理系统 开发
# 图书管理系统 书籍类型--书籍的作者--书籍的出版社---书籍管理
#             用户管理--客户管理--操作处理--主题的设置
# Qt 与 Mysql CRUD操作
# Md5加密，正则表达式处理、日期处理
# 需要完善的内容：  1、添加书籍的时候，书号正则表达式处理 978-7-115-39227-5
#                2、添加用户的时候， 邮箱正则表达式处理
#                3、添加每日操作的时候， 书名、客户从数据库中获取，参照添加图书时候的出版社、作者
#                4、界面美观优化
# 最后打包发布--exe文件（录制视频）
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
from dbutil import get_conn, close_conn
import hashlib
import re
import datetime
from xlsxwriter  import *
# 15:25 -- 15:35 休息

# UI--Logic分离
ui, _ = loadUiType('main.ui')
login, _ = loadUiType('login.ui')


class LoginAPP(QWidget, login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.loginbutton.clicked.connect(self.handel_login)
        style = open("themes/darkorange.css", 'r')
        style = style.read()
        self.setStyleSheet(style)

    # MD5处理
    def md5(self, arg):
        hash = hashlib.md5(bytes("禾木AI", encoding="utf-8"))
        hash.update(bytes(arg, encoding='utf-8'))
        return hash.hexdigest()

    def handel_login(self):
            conn = get_conn()
            cur = conn.cursor()
            sql = "select * from users where user_name=%s and user_pwd=%s"
            user_name = self.username.text()
            pwd = self.pwd.text()
            pwd = self.md5(pwd)
            cur.execute(sql, (user_name, pwd))
            data = cur.fetchone()
            if data:
                self.main_app = MainApp()
                self.close()
                self.main_app.show()

            else:
                self.error_message.setText("用户名或密码错误，重新输入")


class MainApp(QMainWindow, ui):

    # 定义构造方法
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_ui_change()
        self.handle_buttons()
        self.show_category()
        self.show_author()
        self.show_publisher()
        self.show_category_combobox()
        self.show_author_combobox()
        self.show_publisher_combobox()
        self.show_books()
        self.show_client()
        self.show_all_operations()

    # UI变化处理
    def handle_ui_change(self):
        self.hide_themes()
        self.tabWidget.tabBar().setVisible(False)

    # 所有Button的消息与槽的通信
    def handle_buttons(self):
        self.themeButton.clicked.connect(self.show_themes)
        self.theme_change_Button.clicked.connect(self.hide_themes)
        self.bookButton.clicked.connect(self.open_book_tab)
        self.settingButton.clicked.connect(self.open_setting_tab)
        self.userButton.clicked.connect(self.open_user_tab)
        self.add_category_Button.clicked.connect(self.add_category)
        self.add_author_Button.clicked.connect(self.add_author)
        self.add_publisher_Button.clicked.connect(self.add_publisher)
        self.add_book_save_Button.clicked.connect(self.add_book)
        self.editor_book_search_Button.clicked.connect(self.search_book)
        self.editor_book_save_Button.clicked.connect(self.editor_book)
        self.editor_book_delete_Button.clicked.connect(self.delete_book)
        self.dark_orange_button.clicked.connect(self.dark_orange_theme)
        self.dark_blue_button.clicked.connect(self.dark_blue_theme)
        self.dark_gray_button.clicked.connect(self.dark_gray_theme)
        self.qdark_button.clicked.connect(self.qdark_theme)
        self.add_user_button.clicked.connect(self.add_user)
        self.login_button.clicked.connect(self.user_login)
        self.editor_user_button.clicked.connect(self.editor_user)
        self.clientButton.clicked.connect(self.open_client_tab)
        self.add_client_button.clicked.connect(self.add_client)
        self.search_client_button.clicked.connect(self.select_client)
        self.update_client_button.clicked.connect(self.editor_client)
        self.delete_client_button.clicked.connect(self.delete_client)
        self.add_operation.clicked.connect(self.handel_day_operation)
        self.dayButton.clicked.connect(self.open_day_operation_tab)
        self.export_button.clicked.connect(self.export_day_operations)

    # 主题的显示
    def show_themes(self):
        self.theme_groupBox.show()

    # 主题的隐藏
    def hide_themes(self):
        self.theme_groupBox.hide()

    # 选项卡联动
    def open_book_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def open_setting_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def open_user_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_client_tab(self):
        self.tabWidget.setCurrentIndex(3)

    def open_day_operation_tab(self):
        self.tabWidget.setCurrentIndex(4)

    # 1、添加类别
    def add_category(self):
        #  数据库操作流程
        # 1、获取连接
        conn = get_conn()
        # 2、获取cursor
        cur = conn.cursor()
        # 3、SQl语句
        sql = "insert into category(category_name) values(%s)"
        category_name = self.add_category_name.text()
        # 4、执行语句
        cur.execute(sql, (category_name,))
        # 5、insert、update、delete必须显示提交
        conn.commit()
        # 6、关闭资源
        close_conn(conn, cur)
        # 7、消息提示
        self.statusBar().showMessage('类别添加成功！')
        self.add_category_name.setText('')
        self.show_category()

    # 显示已有类别，并且添加完毕后直接可以看到
    def show_category(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = "select category_name from category"
        cur.execute(sql)
        data = cur.fetchall()

        if data:
            self.category_table.setRowCount(0)
            self.category_table.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.category_table.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.category_table.rowCount()
                self.category_table.insertRow(row_position)

    # 添加作者
    def add_author(self):
        #  数据库操作流程
        # 1、获取连接
        conn = get_conn()
        # 2、获取cursor
        cur = conn.cursor()
        # 3、SQl语句
        sql = "insert into author(author_name) values(%s)"
        author_name = self.add_author_name.text()
        # 4、执行语句
        cur.execute(sql, (author_name,))
        # 5、insert、update、delete必须显示提交
        conn.commit()
        # 6、关闭资源
        close_conn(conn, cur)
        # 7、消息提示
        self.statusBar().showMessage('作者添加成功！')
        self.add_author_name.setText('')
        self.show_author()

    # 显示所有作者
    def show_author(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = "select author_name from author"
        cur.execute(sql)
        data = cur.fetchall()

        if data:
            self.author_table.setRowCount(0)
            self.author_table.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.author_table.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.author_table.rowCount()
                self.author_table.insertRow(row_position)

    # 添加出版社
    def add_publisher(self):
        #  数据库操作流程
        # 1、获取连接
        conn = get_conn()
        # 2、获取cursor
        cur = conn.cursor()
        # 3、SQl语句
        sql = "insert into publisher(publisher_name) values(%s)"
        publisher_name = self.add_publisher_name.text()
        # 4、执行语句
        cur.execute(sql, (publisher_name,))
        # 5、insert、update、delete必须显示提交
        conn.commit()
        # 6、关闭资源
        close_conn(conn, cur)
        # 7、消息提示
        self.statusBar().showMessage('作者添加成功！')
        self.add_publisher_name.setText('')
        self.show_publisher()

    # 显示出版社信息
    def show_publisher(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = "select publisher_name from publisher"
        cur.execute(sql)
        data = cur.fetchall()

        if data:
            self.publisher_table.setRowCount(0)
            self.publisher_table.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.publisher_table.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.publisher_table.rowCount()
                self.publisher_table.insertRow(row_position)

    # 将基础数据和combobox绑定
    def show_category_combobox(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = "select category_name from category"
        cur.execute(sql)
        data = cur.fetchall()

        if data:
            self.add_book_category.clear()
            self.editor_book_category.clear()
            for category in data:
                self.add_book_category.addItem(category[0])
                self.editor_book_category.addItem(category[0])

    def show_author_combobox(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = "select author_name from author"
        cur.execute(sql)
        data = cur.fetchall()

        if data:
            self.add_book_author.clear()
            self.editor_book_author.clear()
            for author in data:
                self.add_book_author.addItem(author[0])
                self.editor_book_author.addItem(author[0])

    def show_publisher_combobox(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = "select publisher_name from publisher"
        cur.execute(sql)
        data = cur.fetchall()

        if data:
            self.add_book_publisher.clear()
            self.editor_book_publisher.clear()
            for publisher in data:
                self.add_book_publisher.addItem(publisher[0])
                self.editor_book_publisher.addItem(publisher[0])

    # 1、添加图书 ,插入小数的问题
    # 2、正则表达式问题 后续
    def add_book(self):
        #  数据库操作流程
        # 1、获取连接
        conn = get_conn()
        # 2、获取cursor
        cur = conn.cursor()
        # 3、SQl语句
        sql = "insert into book(book_name, book_description, book_code,book_category, " \
              "book_author, book_publisher, book_price) values(%s, %s, %s, %s, %s, %s, %s)"
        book_name = self.add_book_name.text()
        book_description = self.add_book_desc.toPlainText()
        book_code = self.add_book_code.text()
        book_category = self.add_book_category.currentText()
        book_author = self.add_book_author.currentText()
        book_publisher = self.add_book_publisher.currentText()
        book_price = self.add_book_price.text()
        # 4、执行语句
        cur.execute(sql, (book_name, book_description, book_code, book_category,
                          book_author, book_publisher, book_price))
        # 5、insert、update、delete必须显示提交
        conn.commit()
        # 6、关闭资源
        close_conn(conn, cur)
        self.add_book_name.setText('')
        self.add_book_desc.setPlainText('')
        self.add_book_code.setText('')
        self.add_book_category.setCurrentIndex(0)
        self.add_book_author.setCurrentIndex(0)
        self.add_book_publisher.setCurrentIndex(0)
        self.add_book_price.setText('')
        self.statusBar().showMessage('图书添加成功！')
        self.add_publisher_name.setText('')
        self.show_books()

    # 查找书籍
    def search_book(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = "select * from book where book_name = %s"
        book_name = self.editor_search_name.text()
        cur.execute(sql, (book_name, ))
        data = cur.fetchone()
        if data:
            self.editor_book_name.setText(data[1])
            self.editor_book_desc.setPlainText(data[2])
            self.editor_book_category.setCurrentText(data[3])
            self.editor_book_author.setCurrentText(data[4])
            self.editor_book_publisher.setCurrentText(data[5])
            self.editor_book_price.setText(str(data[6]))
            self.editor_book_code.setText(data[7])

        else:
            self.statusBar().showMessage('没有这个书籍')

    # 修改书籍
    def editor_book(self):
        #  数据库操作流程
        # 1、获取连接
        conn = get_conn()
        # 2、获取cursor
        cur = conn.cursor()
        # 3、SQl语句
        sql = "update book set book_name=%s, book_description=%s, book_code=%s,book_category=%s, " \
              "book_author=%s, book_publisher=%s, book_price=%s  where book_name=%s"
        book_name = self.editor_book_name.text()
        book_description = self.editor_book_desc.toPlainText()
        book_code = self.editor_book_code.text()
        book_category = self.editor_book_category.currentText()
        book_author = self.editor_book_author.currentText()
        book_publisher = self.editor_book_publisher.currentText()
        book_price = self.editor_book_price.text()
        book_old_name = self.editor_search_name.text()
        # 4、执行语句
        cur.execute(sql, (book_name, book_description, book_code, book_category,
                          book_author, book_publisher, book_price, book_old_name))
        # 5、insert、update、delete必须显示提交
        conn.commit()
        self.show_books()
        self.statusBar().showMessage('图书修改成功！')

    # 删除书籍
    def delete_book(self):
        #  数据库操作流程
        # 1、获取连接
        conn = get_conn()
        # 2、获取cursor
        cur = conn.cursor()
        sql = "delete from book where book_name = %s"
        book_name = self.editor_book_name.text()

        warning = QMessageBox.warning(self, '删除图书', '你确定要删除',
                                      QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            cur.execute(sql, (book_name, ))
            conn.commit()
            close_conn(conn, cur)
            self.show_books()
            self.statusBar().showMessage('图书成功删除')

    # 获取所有图书
    def show_books(self):
        #  数据库操作流程
        # 1、获取连接
        conn = get_conn()
        # 2、获取cursor
        cur = conn.cursor()
        sql = "select book_code, book_name, book_description, book_category," \
              " book_author, book_publisher, book_price from book"
        cur.execute(sql)
        data = cur.fetchall()

        self.book_table.setRowCount(0)
        self.book_table.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.book_table.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_postion = self.book_table.rowCount()
            self.book_table.insertRow(row_postion)

    # 主题设置
    def dark_blue_theme(self):
        style = open("themes/darkblue.css", 'r')
        style = style.read()
        self.setStyleSheet(style)

    # 主题设置
    def dark_gray_theme(self):
        style = open("themes/darkgray.css", 'r')
        style = style.read()
        self.setStyleSheet(style)

    # 主题设置
    def dark_orange_theme(self):
        style = open("themes/darkorange.css", 'r')
        style = style.read()
        self.setStyleSheet(style)

    # 主题设置
    def qdark_theme(self):
        style = open("themes/qdark.css", 'r')
        style = style.read()
        self.setStyleSheet(style)

    ####################################################
    ###########用户管理#################################
    def add_user(self):
        #  数据库操作流程
        # 1、获取连接
        conn = get_conn()
        # 2、获取cursor
        cur = conn.cursor()
        # 3、SQl语句
        sql = "insert into users(user_name, user_pwd, user_email) values(%s, %s, %s)"
        user_name = self.add_user_name.text()
        user_email = self.add_user_email.text()
        user_pwd = self.add_user_pwd.text()
        user_confirm_pwd = self.add_user_confirm_pwd.text()
        self.error_message.setText("")
        if user_pwd == user_confirm_pwd:
            # 加盐
            hash = hashlib.md5(bytes("禾木AI", encoding="utf-8"))
            hash.update(bytes(user_pwd, encoding="utf-8"))
            user_pwd_hash = hash.hexdigest()
            # 4、执行语句
            cur.execute(sql, (user_name, user_pwd_hash, user_email))
            # 5、insert、update、delete必须显示提交
            conn.commit()
            # 6、关闭资源
            close_conn(conn, cur)
            # 7、消息提示
            self.statusBar().showMessage('用户添加成功！')
            self.add_user_name.setText('')
            self.add_user_email.setText('')
            self.add_user_pwd.setText('')
            self.add_user_confirm_pwd.setText('')
        else:
            self.error_message.setText("两次密码不一致")
            self.add_user_pwd.setText('')
            self.add_user_confirm_pwd.setText('')


    # MD5处理
    def md5(self, arg):
        hash = hashlib.md5(bytes("禾木AI", encoding="utf-8"))
        hash.update(bytes(arg, encoding='utf-8'))
        return hash.hexdigest()

    # 登录处理
    def user_login(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = "select * from users where user_name=%s and user_pwd=%s"
        old_user_name = self.old_user_name.text()
        editor_pwd = self.editor_pwd.text()
        pwd = self.md5(editor_pwd)
        cur.execute(sql, (old_user_name, pwd))
        data = cur.fetchone()

        if data:
            self.user_groupBox.setEnabled(True)
            self.editor_user_name.setText(data[1])
            self.editor_user_email.setText(data[3])
            # print(data)

    # 修改用户信息
    def editor_user(self):
        old_name = self. old_user_name.text()
        new_name = self.editor_user_name.text()
        new_email = self.editor_user_email.text()
        user_pwd = self.eidtor_user_pwd.text()
        user_confirm_pwd = self.editor_user_confirm_pwd.text()
        if user_pwd == user_confirm_pwd:
            #  数据库操作流程
            # 1、获取连接
            conn = get_conn()
            # 2、获取cursor
            cur = conn.cursor()

            if user_pwd == user_confirm_pwd:
                # 加盐
                hash = hashlib.md5(bytes("禾木AI", encoding="utf-8"))
                hash.update(bytes(user_pwd, encoding="utf-8"))
                user_pwd_hash = hash.hexdigest()
                sql = "update users set user_name=%s, user_email=%s, user_pwd=%s where user_name=%s"
                # 4、执行语句
                cur.execute(sql, (new_name, new_email, user_pwd_hash, old_name))
                # 5、insert、update、delete必须显示提交
                conn.commit()
                # 6、关闭资源
                close_conn(conn, cur)
                self.statusBar().showMessage('用户修改成功！')
                self.user_groupBox.setEnabled(False)
        else:
            self.statusBar().showMessage('两次密码不一致！')

    #######################################################
    #######################client操作#######################

    def add_client(self):
        #  数据库操作流程
        # 1、获取连接
        conn = get_conn()
        # 2、获取cursor
        cur = conn.cursor()
        # 3、SQl语句
        sql = "insert into client(client_name, client_phone, client_id) values(%s, %s, %s)"
        client_name = self.add_client_name.text()
        client_phone = self.add_client_phone.text()
        client_id = self.add_client_id.text()

        # 4、执行语句
        cur.execute(sql, (client_name, client_phone, client_id))
        # 5、insert、update、delete必须显示提交
        conn.commit()
        # 6、关闭资源
        close_conn(conn, cur)
        # 7、消息提示
        self.statusBar().showMessage('客户添加成功！')
        self.add_client_name.setText('')
        self.add_client_phone.setText('')
        self.add_client_id.setText('')
        self.show_client()

    # 显示所有客户
    def show_client(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = "select client_name, client_phone, client_id from client"
        cur.execute(sql)
        data = cur.fetchall()

        if data:
            self.client_table.setRowCount(0)
            self.client_table.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.client_table.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.client_table.rowCount()
                self.client_table.insertRow(row_position)

    def select_client(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = "select client_name, client_phone, client_id from client where client_id = %s"
        old_client_id = self.old_client_id.text()
        cur.execute(sql, (old_client_id, ))
        data = cur.fetchone()

        if data:
            self.editor_client_name.setText(data[0])
            self.editor_client_phone.setText(data[1])
            self.editor_client_id.setText(data[2])

    # 修改用户信息
    def editor_client(self):
        old_client_id = self.old_client_id.text()
        client_name = self.editor_client_name.text()
        client_phone = self.editor_client_phone.text()
        client_id = self.editor_client_id.text()
        regex = re.compile(r"(^0\d{2,3}-\d{7,8}$)")
        if re.match(regex, client_phone):
            conn = get_conn()
            # 2、获取cursor
            cur = conn.cursor()
            # 3、SQl语句
            sql = "update client set client_name=%s, client_phone=%s, client_id=%s " \
                  "where client_id=%s"

            # 4、执行语句
            cur.execute(sql, (client_name, client_phone, client_id, old_client_id))
            # 5、insert、update、delete必须显示提交
            conn.commit()
            # 6、关闭资源
            close_conn(conn, cur)
            self.statusBar().showMessage("修改成功！")
            self.show_client()
        else:
            self.statusBar().showMessage("电话格式位区号-电话")

    def delete_client(self):
        old_client_id = self.old_client_id.text()
        warning = QMessageBox.warning(self, "删除客户", "你确定删除吗?",
                                      QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            conn = get_conn()
            # 2、获取cursor
            cur = conn.cursor()
            # 3、SQl语句
            sql = "delete from client where client_id = %s"

            # 4、执行语句
            cur.execute(sql, (old_client_id, ))
            # 5、insert、update、delete必须显示提交
            conn.commit()
            close_conn(cur, conn)
            self.statusBar().showMessage("删除客户成功！")
            self.show_client()

    # 如何进行日期类型的操作
    ##### 日常操作，需要完善从数据库中获取书名和客户名称 ######
    def handel_day_operation(self):
        book_name = self.book_name.text()
        client_name = self.client_name.text()
        operate_type = self.tpye_combox.currentText()
        day_number = self.day_combox.currentIndex() + 1
        today_date = datetime.date.today()
        to_day = today_date + datetime.timedelta(days=day_number)

        # 数据库操作
        conn = get_conn()
        cur = conn.cursor()
        sql = "insert into dayoperations(book_name, client_name, type, days, day_from, day_to)" \
              "values(%s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (book_name, client_name, operate_type, day_number, today_date, to_day))
        conn.commit()
        close_conn(conn, cur)
        self.statusBar().showMessage("操作添加成功！")
        self.show_all_operations()

    # 显示所有的操作
    def show_all_operations(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = "select book_name, client_name, type, day_from, day_to from dayoperations"
        cur.execute(sql)
        data = cur.fetchall()

        if data:
            self.operation_table.setRowCount(0)
            self.operation_table.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.operation_table.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.operation_table.rowCount()
                self.operation_table.insertRow(row_position)

    def export_day_operations(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = "select book_name, client_name, type, day_from, day_to from dayoperations"
        cur.execute(sql)
        data = cur.fetchall()

        wb = Workbook("day_operations.xlsx")
        sheet1 = wb.add_worksheet()

        sheet1.write(0, 0, "书名")
        sheet1.write(0, 1, "客户")
        sheet1.write(0, 2, "类型")
        sheet1.write(0, 3, "开始时间")
        sheet1.write(0, 4, "结束时间")

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1

        wb.close()
        self.statusBar().showMessage("数据导出成功！")


def main():
    app = QApplication(sys.argv)
    window = LoginAPP()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
