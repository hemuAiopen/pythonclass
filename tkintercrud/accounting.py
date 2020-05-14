from tkinter import ttk
from tkinter import *
import sqlite3


class Accounting:

    # 数据库名字
    db_name = 'database.db'

    # 初始化操作
    def __init__(self, window):
        self.win = window
        self.win.title('Tkinter数据库操作')

        # 创建容器
        frame = LabelFrame(self.win, text='日常收支记录')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # 输入项目
        Label(frame, text='项目').grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)
        Label(frame, text='费用').grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)
        Label(frame, text='类别').grid(row=3, column=0)
        self.type = ttk.Combobox(frame, values=['收入', '支出'], state='readonly')
        self.type.grid(row=3, column=1)
        self.type.current(0)

        ttk.Button(frame, text='保存', command=self.add_accounting).grid(row=4, columnspan=2, sticky=W+E)

        # 数据操作结果的提示信息
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W+E)

        # treeview进行表格信息显示
        self.tree = ttk.Treeview(height=10, columns=("#0", "#1", "#2"))
        self.tree.grid(row=4, column=0, columnspan=3)
        self.tree.heading("#0", text='项目', anchor=CENTER)
        self.tree.heading("#1", text='费用', anchor=CENTER)
        self.tree.heading("#2", text='类型', anchor=CENTER)

        ttk.Button(text='删除', command=self.delete_accounting).grid(row=5, column=0, sticky= W+E)
        ttk.Button(text='编辑', command=self.edit_accounting_win).grid(row=5, column=1, sticky=W + E)
        self.get_accounting()

    # 数据库操作方法
    def run_query(self, query, params=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = conn.execute(query, params)
            conn.commit()
            return result

    # 数据完整性验证
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    # 数据添加处理
    def add_accounting(self):
        if self.validation():
            query = "insert into accounting(name, price, type) values(?, ?, ?)"
            params = (self.name.get(), self.price.get(), self.type.get())
            self.run_query(query, params)
            self.message['text'] = "{}添加成功".format(self.name.get())
            self.get_accounting()
        else:
            self.message['text'] = '项目和费用不能为空'

    # 显示所有项目
    def get_accounting(self):
        # 重绘表格内容
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        query = "select * from accounting order by type"
        db_rows = self.run_query(query)

        # 填充表格
        for row in db_rows:
            self.tree.insert("", 0, text=row[1], values=(row[2], row[3]))

    # 删除项目
    def delete_accounting(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = '请选择操作项目'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'delete from accounting where name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = '{}删除成功'.format(name)
        self.get_accounting()

    # 修改项目
    # 修改的窗体实现
    def edit_accounting_win(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = '请选择操作项目'
            return
        old_name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        old_type = self.tree.item(self.tree.selection())['values'][1]

        self.edit_win = Toplevel()
        self.edit_win.title = '编辑项目'
        # 原来的项目
        Label(self.edit_win, text='原来项目').grid(row=0, column=1)
        Entry(self.edit_win, textvariable=StringVar(self.edit_win, value=old_name), state='readonly').grid(row=0, column=2)

        Label(self.edit_win, text='新的项目').grid(row=1, column=1)
        new_name = Entry(self.edit_win)
        new_name.grid(row=1, column=2)

        Label(self.edit_win, text='原来费用').grid(row=2, column=1)
        Entry(self.edit_win, textvariable=StringVar(self.edit_win, value=old_price), state='readonly').grid(row=2, column=2)

        Label(self.edit_win, text='新的费用').grid(row=3, column=1)
        new_price = Entry(self.edit_win)
        new_price.grid(row=3, column=2)

        Label(self.edit_win, text='类别').grid(row=4, column=1)
        new_type = ttk.Combobox(self.edit_win, values=['收入', '支出'], state='readonly')
        new_type.grid(row=4, column=2)
        new_type.set(old_type)

        Button(self.edit_win, text='更新', command=lambda: self.edit_record(new_name.get(), old_name, new_price.get(), old_price, new_type.get(), old_type)).grid(row=5, column=2, sticky=W+E)

        self.edit_win.mainloop()

    # 数据修改处理
    def edit_record(self, new_name, old_name, new_price, old_price, new_type, old_type):
        query = "update accounting set name=?, price=?,  type=? where name=? and price=? and type=?"
        params = (new_name, new_price, new_type, old_name, old_price, old_type)
        self.run_query(query, params)
        self.edit_win.destroy()
        self.message['text'] = "{}更新成功".format(old_name)
        self.get_accounting()


if __name__ == '__main__':
    window = Tk()
    application = Accounting(window)
    window.mainloop()
