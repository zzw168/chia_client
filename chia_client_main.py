import datetime
import json
import os
import subprocess
import sys
import time

import pymysql
import pyperclip
import requests

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QAbstractItemView, QPushButton, \
    QMenu, QMessageBox
from requests import request

import chia_client_ui

# host = '127.0.0.1'
host = '192.168.88.211'
# user = 'chia'
# password = "2pWBMZdwxRjXMY4p"
user = 'root'
password = "root"
# password = "XpTmemaEHC53SHHz"
database = 'chia'

global message_init


class My_Gui(chia_client_ui.Ui_MainWindow):  # 自定义窗口样式
    def __init__(self):
        super().__init__()

        # Custom output stream.

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        table = self.tableWidget

        # font = QFont('微软雅黑', 20)
        # font.setBold(True)  # 设置字体加粗
        # table.horizontalHeader().setFont(font)  # 设置表头字体
        # 为font设置的字体样式

        # table.setFrameShape(QFrame.NoFrame)  ##设置无表格的外框
        # table.horizontalHeader().setFixedHeight(25)  ##设置表头高度
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # 设置第五列宽度自动调整，充满屏幕
        # table.horizontalHeader().setStretchLastSection(True)  ##设置最后一列拉伸至最大
        table.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只可以单选，可以使用ExtendedSelection进行多选
        table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置 不可选择单个单元格，只可选择一行。
        table.horizontalHeader().resizeSection(0, 80)  # 设置第一列的宽度为200
        table.horizontalHeader().resizeSection(1, 160)  # 设置第一列的宽度为200
        table.horizontalHeader().resizeSection(2, 30)  # 设置第一列的宽度为200
        table.horizontalHeader().resizeSection(3, 50)  # 设置第一列的宽度为200

        # table.setColumnCount(5)  ##设置表格一共有五列
        # table.setHorizontalHeaderLabels(['id', '姓名', '年龄', '学号', '地址'])  # 设置表头文字

        # table.horizontalHeader().setSectionsClickable(False)  # 可以禁止点击表头的列
        # table.sortItems(0, Qt.DescendingOrder)  # 设置按照第二列自动降序排序
        # table.sortItems(0, Qt.AscendingOrder)  # 设置按照第一列自动升序排序
        # table.horizontalHeader().setStyleSheet('QHeaderView::section{background:white}')  # 设置表头的背景色为绿色
        # table.setColumnHidden(1, True)  # 将第二列隐藏
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可更改
        table.setSortingEnabled(False)  # 设置表头可以自动排序
        # 允许弹出菜单
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        # 将信号请求连接到槽（单击鼠标右键，就调用方法）
        table.customContextMenuRequested.connect(self.generateMenu)

        table_2 = self.tableWidget_2
        # table.horizontalHeader().setStretchLastSection(True)  ##设置最后一列拉伸至最大
        table_2.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只可以单选，可以使用ExtendedSelection进行多选
        table_2.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置 不可选择单个单元格，只可选择一行。
        table_2.horizontalHeader().resizeSection(0, 80)  # 设置第一列的宽度为200
        table_2.horizontalHeader().resizeSection(1, 150)  # 设置第一列的宽度为200
        table_2.horizontalHeader().resizeSection(2, 80)  # 设置第一列的宽度为200
        table_2.horizontalHeader().resizeSection(3, 100)  # 设置第一列的宽度为200
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可更改

        table_4 = self.tableWidget_4
        # table.horizontalHeader().setStretchLastSection(True)  ##设置最后一列拉伸至最大
        table_4.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只可以单选，可以使用ExtendedSelection进行多选
        table_4.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置 不可选择单个单元格，只可选择一行。
        table_4.horizontalHeader().resizeSection(0, 80)  # 设置第一列的宽度为200
        table_4.horizontalHeader().resizeSection(1, 80)  # 设置第一列的宽度为200
        table_4.horizontalHeader().resizeSection(2, 100)  # 设置第一列的宽度为200
        table_4.horizontalHeader().resizeSection(3, 200)  # 设置第一列的宽度为200
        table_4.horizontalHeader().resizeSection(4, 100)  # 设置第一列的宽度为200
        table_4.horizontalHeader().resizeSection(5, 200)  # 设置第一列的宽度为200
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可更改
        table_4.setSortingEnabled(False)  # 设置表头可以自动排序
        # pos为点击的位置

    def generateMenu(self, pos):
        print(pos)
        table = self.tableWidget

        menu = QMenu()
        item1 = menu.addAction("复制IP地址")
        # item2 = menu.addAction("菜单2")
        # item3 = menu.addAction("菜单3")
        # 使菜单在正常位置显示
        screenPos = table.mapToGlobal(pos)

        # 单击一个菜单项就返回，使之被阻塞
        action = menu.exec(screenPos)
        if action == item1:
            # print('选择菜单1', table.item(table.currentRow(), 0).text())
            pyperclip.copy(table.item(table.currentRow(), 1).text())  # 把text字符串中的字符复制到剪切板
            text = pyperclip.paste()  # 把剪切板上的字符串复制到text
        # if action == item2:
        #     print('选择菜单2', table.item(table.currentRow(), 0).text())
        # if action == item3:
        #     print('选择菜单3', table.item(table.currentRow(), 0).text())
        else:
            return


def Get_userInfo():  # 获取 userlist 表数据 ，并更新客户机列表
    global message_init
    # SQL 查询语句
    sql = "SELECT * FROM %s ORDER BY name" % ('userlist')
    try:
        # 获取所有记录列表
        results = db_select(sql)
        message_init = results
        table = ui.tableWidget
        t = table.rowCount()
        results_count = len(results)
        if t != results_count:
            table.setRowCount(results_count)
            if t < results_count:
                for j in range(t, results_count):
                    for k in range(0, table.columnCount()):
                        zero = QTableWidgetItem('0')
                        zero.setTextAlignment(Qt.AlignCenter)
                        table.setItem(j, k, zero)  # 补齐列表空间
        for i in range(0, len(results)):
            if table.item(i, 1).text() != str(results[i][1]):
                ip = QTableWidgetItem(str(results[i][1]))
                ip.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 1, ip)
            if table.item(i, 0).text() != str(results[i][2]):
                name = QTableWidgetItem(str(results[i][2]))
                name.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 0, name)
            if table.item(i, 2).text() != str(results[i][6]):
                num = QTableWidgetItem(str(results[i][6]))
                num.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 2, num)

            end = int(datetime.datetime.now().timestamp())

            if int(results[i][4]) < end - 60:
                s = '离线'

            else:
                if results[i][7] == 1:
                    s = '异常'
                else:
                    s = ' '
            if table.item(i, 3).text() != s:
                isbug = QTableWidgetItem(s)
                isbug.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 3, isbug)
            if table.item(i, 4).text() != str(results[i][8]):
                version = QTableWidgetItem(str(results[i][8]))
                version.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 4, version)

        table.setFocus()
        ui.label_num.setText("客户机数量: %d" % t)
    except:
        print("Error: unable to fecth data")


def ping_host():  # 开启线程
    if thread_data.run_flg == False:
        thread_data.run_flg = True
        thread_data.start()
    else:
        thread_data.run_flg = not (thread_data.run_flg)

    if thread_message.run_flg == False:
        thread_message.run_flg = True
        thread_message.start()
    else:
        thread_message.run_flg = not (thread_message.run_flg)


def signal_accept_data(i):
    select_change()


class data_Thread(QThread):  # 单个客户机详细资料线程
    _signal = pyqtSignal(int)  # 定义信号类型为整型

    def __init__(self):
        super(data_Thread, self).__init__()
        self.run_flg = False

    def run(self):
        global time_pass
        time_pass = 1
        while True:
            if self.run_flg:
                time_pass += 1
                self._signal.emit(1)  # 发射信号

            time.sleep(1)


def signal_accept_message(i):
    Get_userInfo()
    disk_full()


class message_Thread(QThread):  # 所有客户机总体情况线程
    _signal = pyqtSignal(int)  # 定义信号类型为整型

    def __init__(self):
        super(message_Thread, self).__init__()
        self.run_flg = False

    def run(self):
        while True:
            if self.run_flg:
                self._signal.emit(0)  # 发射信号
            time.sleep(10)


def select_change():  # 跟新单个客户机的P盘信息
    global time_pass
    global message_init

    table = ui.tableWidget
    row = table.currentRow()
    if row == -1:
        return False
    name = table.item(row, 0).text()
    ui.lineEdit.setText(name)
    ip = table.item(row, 1).text()
    if time_pass < 11:
        table2 = ui.tableWidget_2
        row = table2.rowCount()
        if row != -1:
            for i in range(0, row):
                dt = table2.item(i, 1).text()
                d_time = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
                start = int(time.mktime(d_time.timetuple()))
                end = int(datetime.datetime.now().timestamp())
                seconds = end - start
                m, s = divmod(seconds, 60)
                h, m = divmod(m, 60)
                dt = "%d:%02d:%02d" % (h, m, s)
                if table2.item(i, 2).text() != str(dt):
                    update_time = QTableWidgetItem(str(dt))
                    update_time.setTextAlignment(Qt.AlignCenter)
                    table2.setItem(i, 2, update_time)
    else:
        time_pass = 1
        # SQL 查询语句
        # sql = "SELECT * FROM %s WHERE ip='%s'" % ('userlist', ip)
        # print(sql)
        try:
            # results = db_select(sql)
            for i in range(0, len(message_init)):
                if message_init[i][1] == ip and message_init[i][2] == name:
                    results = message_init[i]
                    break
                else:
                    results = 0
            if results == 0:
                return False
            # 客户机信息——————————————————————————————————————————————————————————————————
            info = results[3]
            dict_info = json.loads(info)
            cpu_num = dict_info['cpu_num']
            ppk = dict_info['ppk']
            fpk = dict_info['fpk']
            num = dict_info['num']
            name = dict_info['name']
            username = dict_info['username']
            sum = dict_info['sum']

            if ui.lineEdit_name.text() != str(name):
                ui.lineEdit_name.setText(str(name))
            if ui.lineEdit_username.text() != str(username):
                ui.lineEdit_username.setText(str(username))
            if ui.lineEdit_fpk.text() != str(fpk):
                ui.lineEdit_fpk.setText(str(fpk))
            if ui.lineEdit_ppk.text() != str(ppk):
                ui.lineEdit_ppk.setText(str(ppk))
            if ui.lineEdit_num.text() != str(num):
                ui.lineEdit_num.setText(str(num))
            if ui.lineEdit_sum.text() != str(sum):
                ui.lineEdit_sum.setText(str(sum))
            if ui.lineEdit_cpu.text() != str(cpu_num):
                ui.lineEdit_cpu.setText(str(cpu_num))
            # 硬盘信息————————————————————————————————————————————————————————————————————————
            io_info = results[9]
            dict_io_info = json.loads(io_info)
            print(dict_io_info)
            table = ui.tableWidget_3
            t = table.rowCount()
            len_data = len(dict_io_info)
            if t != len_data:
                table.setRowCount(len_data)
                if t < len_data:
                    for j in range(t, len_data):
                        for k in range(0, table.columnCount()):
                            zero = QTableWidgetItem('0')
                            zero.setTextAlignment(Qt.AlignCenter)
                            table.setItem(j, k, zero)

            for i in range(0, len_data):
                if table.item(i, 0).text() != str(dict_io_info[i]['sun_size']):
                    sun_size = QTableWidgetItem(str(dict_io_info[i]['sun_size']))
                    sun_size.setTextAlignment(Qt.AlignCenter)
                    table.setItem(i, 0, sun_size)
                if table.item(i, 1).text() != str(dict_io_info[i]['k_size']):
                    k_size = QTableWidgetItem(str(dict_io_info[i]['k_size']))
                    k_size.setTextAlignment(Qt.AlignCenter)
                    table.setItem(i, 1, k_size)
                if table.item(i, 2).text() != str(dict_io_info[i]['yfb']):
                    yfb = QTableWidgetItem(str(dict_io_info[i]['yfb']))
                    yfb.setTextAlignment(Qt.AlignCenter)
                    table.setItem(i, 2, yfb)
                if table.item(i, 3).text() != str(dict_io_info[i]['path']):
                    path = QTableWidgetItem(str(dict_io_info[i]['path']))
                    path.setTextAlignment(Qt.AlignLeft)
                    table.setItem(i, 3, path)

            # P图进度信息——————————————————————————————————————————————————————————
            data = results[5]
            dict_data = json.loads(data)
            print(dict_data)
            table = ui.tableWidget_2
            t = table.rowCount()
            if t != len(dict_data):
                table.setRowCount(len(dict_data))
                if t < len(dict_data):
                    for j in range(t, len(dict_data)):
                        for k in range(0, table.columnCount()):
                            zero = QTableWidgetItem('0')
                            zero.setTextAlignment(Qt.AlignCenter)
                            table.setItem(j, k, zero)
            for i in range(0, len(dict_data)):
                if table.rowCount() != len(dict_data):
                    table.setRowCount(i + 1)

                time_local = time.localtime(dict_data[i]['addtime'])
                # 转换成新的时间格式(2016-05-05 20:28:54)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                if table.item(i, 1).text() != str(dt):
                    addtime = QTableWidgetItem(dt)
                    addtime.setTextAlignment(Qt.AlignCenter)
                    table.setItem(i, 1, addtime)

                end = int(datetime.datetime.now().timestamp())
                start = dict_data[i]['addtime']
                seconds = end - start
                m, s = divmod(seconds, 60)
                h, m = divmod(m, 60)
                dt = "%d:%02d:%02d" % (h, m, s)
                if table.item(i, 2).text() != str(dt):
                    update_time = QTableWidgetItem(str(dt))
                    update_time.setTextAlignment(Qt.AlignCenter)
                    table.setItem(i, 2, update_time)

                if table.item(i, 3).text() != str('%s%s' % (dict_data[i]['dow'], '%')):
                    dow = QTableWidgetItem('%s%s' % (dict_data[i]['dow'], '%'))
                    dow.setTextAlignment(Qt.AlignCenter)
                    table.setItem(i, 3, dow)

                if table.item(i, 4).text() != str(dict_data[i]['path']):
                    path = QTableWidgetItem(dict_data[i]['path'])
                    path.setTextAlignment(Qt.AlignCenter)
                    table.setItem(i, 4, path)

                if dict_data[i]['staues'] == 0:
                    dt = 'P图中'
                if dict_data[i]['staues'] == 1:
                    dt = 'P图完成'
                if dict_data[i]['staues'] == 2:
                    dt = '完成'
                if dict_data[i]['staues'] == 3:
                    dt = '迁移中'
                if table.item(i, 0).text() != str(dt):
                    staues = QTableWidgetItem(dt)
                    staues.setTextAlignment(Qt.AlignCenter)
                    table.setItem(i, 0, staues)

        except:
            print('列表数据出错！')


def db_run(sql):
    db = pymysql.connect(user=user, password=password, host=host,
                         database=database)
    cur = db.cursor()
    # print(sql)
    try:
        cur.execute(sql)
        db.commit()
    except:
        db.rollback()
    cur.close()
    db.close()


def db_select(sql):
    # 打开数据库连接
    db = pymysql.connect(user=user, password=password, host=host,
                         database=database)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 查询语句
    # sql = "SELECT * FROM %s WHERE ip='%s'" % ('userlist', ip)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print('数据库链接出错！')
    finally:
        cursor.close()
        db.close()
    return results


def delete_btnClick():
    table = ui.tableWidget_5
    num = table.currentRow()
    id = table.item(num, 0).text()
    sql = "DELETE FROM %s WHERE id =%d" % ('disklog', int(id))
    db_run(sql)
    table.removeRow(num)


def disk_full():  # 查询已满的硬盘信息
    # SQL 查询语句
    sql = "SELECT * FROM %s" % ('disklog')
    try:
        results = db_select(sql)
        table = ui.tableWidget_5
        t = table.rowCount()
        len_data = len(results)
        if t != len_data:
            table.setRowCount(len_data)
            if t < len_data:
                for j in range(t, len_data):
                    for k in range(0, table.columnCount() - 1):
                        zero = QTableWidgetItem('0')
                        zero.setTextAlignment(Qt.AlignCenter)
                        table.setItem(j, k, zero)
                    pushButton = QPushButton("删除")
                    pushButton.setStyleSheet("QPushButton{margin:3px};")
                    pushButton.clicked.connect(delete_btnClick)  # 绑定按钮点击事件
                    table.setCellWidget(j, table.columnCount() - 1, pushButton)
        for i in range(0, len_data):

            if table.item(i, 0).text() != str(results[i][0]):
                id = QTableWidgetItem(str(results[i][0]))
                id.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 0, id)
            if table.item(i, 1).text() != str(results[i][1]):
                name = QTableWidgetItem(str(results[i][1]))
                name.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 1, name)
            if table.item(i, 2).text() != str(results[i][2]):
                path = QTableWidgetItem(str(results[i][2]))
                path.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 2, path)
            if table.item(i, 3).text() != '%sG' % str(results[i][3]):
                size = QTableWidgetItem('%sG' % str(results[i][3]))
                size.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 3, size)

    except:
        print('查询硬盘信息出错！')


def ok_data():  # 查询已经完成的P盘任务信息
    name = ui.lineEdit.text()
    if name != None:
        sql = "SELECT * FROM %s WHERE name ='%s' ORDER BY endtime DESC " % ('oklist', name)
        try:
            results = db_select(sql)
            table = ui.tableWidget_4
            len_data = len(results)
            table.setRowCount(len_data)
            for i in range(0, len_data):
                id = QTableWidgetItem(str(results[i][0]))
                id.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 0, id)

                name = QTableWidgetItem(str(results[i][1]))
                name.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 1, name)

                acount = QTableWidgetItem(str(results[i][8]))
                acount.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 2, acount)

                time_local = time.localtime(results[i][3])
                # 转换成新的时间格式(2016-05-05 20:28:54)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                add_time = QTableWidgetItem(str(dt))
                add_time.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 3, add_time)

                seconds = results[i][4] - results[i][3]
                m, s = divmod(seconds, 60)
                h, m = divmod(m, 60)
                t = "%d:%02d:%02d" % (h, m, s)
                add_time = QTableWidgetItem(str(t))
                add_time.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 4, add_time)

                time_local = time.localtime(results[i][4])
                # 转换成新的时间格式(2016-05-05 20:28:54)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                end_time = QTableWidgetItem(str(dt))
                end_time.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 5, end_time)

                to_path = QTableWidgetItem(str(results[i][7]))
                to_path.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 6, to_path)

                file_name = QTableWidgetItem(str(results[i][6]))
                file_name.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 7, file_name)
            # table.sortItems(5, Qt.DescendingOrder)  # 设置按照第二列自动降序排序
        except:
            print("完成数据查询出错")


def load_data():
    global time_pass
    time_pass = 20
    select_change()


def Send_Reboot():
    table = ui.tableWidget
    num = table.currentRow()
    url = table.item(num, 1).text()
    re = QMessageBox.question(MainWindow, "提示", "是否重启 %s" % table.item(num, 0).text(), QMessageBox.Yes |
                              QMessageBox.No, QMessageBox.No)
    if re == QMessageBox.Yes:
        try:
            response = requests.get("http://%s:5000/reboot" % url)
            if response.status_code != 200:
                print(response)
                QMessageBox.question(MainWindow, "提示", "重启 %s 失败" % table.item(num, 0).text(), QMessageBox.Ok)

        except:
            QMessageBox.question(MainWindow, "提示", "正在重启 %s" % table.item(num, 0).text(), QMessageBox.Ok)
            table.item(num, 3).setText("重启中")


def Send_shutdown():
    table = ui.tableWidget
    num = table.currentRow()
    url = table.item(num, 1).text()
    re = QMessageBox.question(MainWindow, "提示", "是否关机 %s" % table.item(num, 0).text(), QMessageBox.Yes |
                              QMessageBox.No, QMessageBox.No)
    if re == QMessageBox.Yes:
        try:
            response = requests.get("http://%s:5000/halt" % url)
            if response.status_code != 200:
                print(response)
                QMessageBox.question(MainWindow, "提示", "关机 %s 失败" % table.item(num, 0).text(), QMessageBox.Ok)

        except:
            QMessageBox.question(MainWindow, "提示", "正在关机 %s" % table.item(num, 0).text(), QMessageBox.Ok)


def Send_UpdateKey():
    table = ui.tableWidget
    num = table.currentRow()
    url = table.item(num, 1).text()
    re = QMessageBox.question(MainWindow, "提示", "是否更改 %s 配置信息" % table.item(num, 0).text(), QMessageBox.Yes |
                              QMessageBox.No, QMessageBox.No)
    if re == QMessageBox.Yes:
        try:
            json_data = {
                "cpu_num": int(ui.lineEdit_cpu.text()),
                "fpk": ui.lineEdit_fpk.text(),
                "is_reboot": 1,
                "name": ui.lineEdit_name.text(),
                "num": int(ui.lineEdit_num.text()),
                "ppk": ui.lineEdit_ppk.text(),
                "sum": int(ui.lineEdit_sum.text()),
                "username": int(ui.lineEdit_username.text()),
            }
            session = requests.session()
            response = session.post("http://%s:5000/e_config" % url, json=json_data)
            print(response)
            if response.status_code == 200:
                QMessageBox.question(MainWindow, "提示", "提交更改 %s 成功！" % table.item(num, 0).text(), QMessageBox.Ok)

        except:
            QMessageBox.question(MainWindow, "提示", "提交更改失败 %s" % table.item(num, 0).text(), QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = My_Gui()
    ui.setupUi(MainWindow)
    MainWindow.show()

    global time_pass

    thread_data = data_Thread()  # 开启线程
    # thread1.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
    thread_data._signal.connect(signal_accept_data)  # 更新单个客户机数据
    thread_data.run_flg = False

    thread_message = message_Thread()  # 开启线程
    # thread1.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
    thread_message._signal.connect(signal_accept_message)
    thread_message.run_flg = False

    table = ui.tableWidget
    table.itemSelectionChanged.connect(load_data)

    ui.pushButton.clicked.connect(ok_data)
    ui.pushButton_reboot.clicked.connect(Send_Reboot)
    ui.pushButton_shutdown.clicked.connect(Send_shutdown)
    ui.pushButton_update.clicked.connect(Send_UpdateKey)

    Get_userInfo()
    ping_host()

    sys.exit(app.exec_())
