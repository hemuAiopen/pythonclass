# 14:30 PyQt5 图书管理系统 开发
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import sys
from dbutil import get_conn, close_conn

# 5.13日 完成 界面设计、code编程联动， 再 作者\出版社添加及显示

# UI--Logic分离
ui, _ = loadUiType('main.ui')


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
        self.add_category_Button.clicked.connect(self.add_category)
        self.add_author_Button.clicked.connect(self.add_author)
        self.add_publisher_Button.clicked.connect(self.add_publisher)

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

    # 数据库处理 16:23--16:33 休息--》数据库操作
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


def main():
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
