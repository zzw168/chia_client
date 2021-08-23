import datetime
import json
import subprocess
import sys
import time
from gevent import pywsgi

import requests
import pymysql
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from flask import Flask, request, json  # 路由挂载包

import chia_server_ui

# host = '127.0.0.1'
host = '192.168.88.211'
# user = 'chia'
# password = "2pWBMZdwxRjXMY4p"
# password = "XpTmemaEHC53SHHz"
user = 'root'
password = 'root'
database = 'chia'

http = Flask(__name__)  # 路由变量


@http.route('/nodisk', methods=['POST', 'GET'])  # 硬盘已满
def nodisk_message():
    if request.method == "POST":
        # message = request.get_data()
        my_json = request.get_json()
        print(my_json)
        if my_json != None:
            sql = "SELECT * FROM disklog WHERE name='%s'" % my_json['name']
            s = db_select(sql)
            print(len(s))
            # print(type(s))
            if len(s) == 0:
                try:
                    sql = "INSERT INTO disklog (name,path,size) VALUES ('%s','%s','%s')" \
                          % (str(my_json['name']), str(my_json['path']), str(my_json['free']))
                    db_run(sql)
                    ui.textEdit_3.append('插入disklog %s 硬盘已满' % (my_json['name']))

                except:
                    print('数据出错')
    return "ok~"


@http.route('/call', methods=['POST', 'GET'])  # 设置接收服务端口
def access_message():
    if request.method == "POST":
        # message = request.get_data()
        my_json = request.get_json()
        print(my_json)
        print(type(my_json))
        my_str = json.dumps(my_json)
        print("1:%s" % my_str)
        if my_json != None:
            try:
                sql = "SELECT * FROM userlist WHERE ip='%s'" % my_json['ip']
                s = db_select(sql)
                print(len(s))
                # print(type(s))
                if len(s) == 0:
                    sql = "INSERT INTO userlist (ip,name,info)" \
                          "VALUES ('%s','%s','%s')" % (str(my_json['ip']), str(my_json['name']),
                                                       my_str)
                    db_run(sql)
                    ui.textEdit_3.append('插入 %s 数据' % (my_json['ip']))
                else:
                    sql = "UPDATE userlist SET ip='%s',name='%s',info='%s' WHERE ip='%s' " % (
                        str(my_json['ip']), str(my_json['name']), my_str, my_json['ip'])
                    db_run(sql)
                    # ui.textEdit_3.append('更新 %s 数据' % (my_json['ip']))
            except:
                print('数据出错')
    return 'ok'
    # ui.textEdit_3.append(message)


def post_json():  # 测试接收客户机数据
    userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    header = {
        # "origin": "https://passport.mafengwo.cn",
        "Referer": '127.0.0.1',
        'User-Agent': userAgent,
    }
    postData = {
        'ip': '192.168.77.254',
        'name': '9-9',
        'cpu_num': 8,
        'fpk': '821ffc73b2c4e9845aab06ee3b58b3b5148209c8bcc647cf3676d9b93a22c98e212429df1a019452a17b48344d65c953',
        'is_reboot': 1,
        'num': 1,
        'ppk': 'xch1dfdsg0v8dfa3hspzhzeauw9667a5zthg6sgdaplh3s0p66e3eysqy0ft6p',
        'sum': 1,
        'username': '261398126',
    }
    s = requests.session()
    # res = s.post(postUrl, data=postData, headers=header, timeout=5)
    res = s.post('http://127.0.0.1:1314/call', json=postData, headers=header)
    print(res.content)
    print(type(res.content))

    post = {
        'type': "cp",
        'name': '9-9',
        'path': 'd:/aaa/',
        'free': '97G',
        'msg': "容量不足"
    }

    res = s.post('http://127.0.0.1:1314/nodisk', json=post)
    print(res.content)
    print(type(res.content))


class My_Gui(chia_server_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)


def db_run(sql):  # 运行数据库操作
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


def db_select(sql):  # 查询数据库操作
    # 打开数据库连接
    db = pymysql.connect(user=user, password=password, host=host,
                         database=database)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    results = ''
    # SQL 查询语句
    # sql = "SELECT * FROM %s WHERE ip='%s'" % ('userlist', ip)
    # print(sql)
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


def run_cmd(cmd):  # 测试主机网络是否通畅
    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    try:
        while process.poll() is None:
            line = process.stdout.readline()
            line = line.strip()
            if line:
                # line.decode("936", 'ignore')
                s = 'ok'
                log = line.decode("936", 'ignore')
                # print(log)
                if log.find('无法访问目标主机') != -1:
                    s = '无法访问目标主机'
                    break
                if log.find('请求超时') != -1:
                    s = '请求超时'
                    break
                if log.find('(100 % 丢失)') != -1:
                    s = '(100 % 丢失)'
                    break
        # # log = process.stdout.read().decode("936", 'ignore')
        # # print(log)
        return s
    except:
        return 'error'


def update_userlist():  # 主动更新用户列表数据
    table = 'userlist'
    sql = 'SELECT * FROM %s' % table
    db_message = db_select(sql)
    message_list = []
    message_list.append('完成获取userlist数据')
    for i in range(0, len(db_message)):
        if db_message[i][1] != None:
            ip = db_message[i][1]
            s = run_cmd('ping %s -n 1' % (ip))
            # print(s)
            if s == 'ok':
                try:
                    r_list = session.get('http://%s:5000/r_list' % ip).content.decode('utf-8')  # 进行中记录
                    my_json = json.loads(r_list)
                    data = json.dumps(my_json['data'])

                    uptime = int(time.time())
                    num = len(my_json['data'])

                    end = int(datetime.datetime.now().timestamp())

                    if uptime < end - 5400:
                        isbug = 1
                    else:
                        isbug = 0

                    io_info = session.get('http://%s:5000/io_info' % ip).content.decode('utf-8')  # 存储介质资料
                    my_json = json.loads(io_info)
                    io_info = json.dumps(my_json['data'])

                    version = session.get('http://%s:5000/version' % ip).content.decode('utf-8')  # 存储介质资料

                    # print(db_message[i][1])
                    sql = "UPDATE %s SET data='%s',uptime='%s',num='%s',isbug='%s',io_info='%s',version='%s' WHERE ip='%s' " % (
                        str(table), data, str(uptime), str(num), str(isbug), io_info, str(version), ip)
                    db_run(sql)

                except:
                    s = '%s 链接数据出错' % db_message[i][2]
                    # print(s)
                # sql = 'SELECT name FROM %s WHERE ip="%s"' % (table,ip)
                # db_m = db_select(sql)
                # print(db_m)
            else:
                s = "%s 掉线 %s" % (ip, s)
                print(s)
            if s != 'ok':
                message_list.append(s)
    return message_list


def signal_accept_data(message_list):
    print(message_list)
    for s in message_list:
        ui.textEdit_2.append(s)


class http_Thread(QThread):
    _signal = pyqtSignal(object)  # 定义信号类型为整型

    def __init__(self):
        super(http_Thread, self).__init__()
        self.run_flg = False

    def run(self):
        # http.run('0.0.0.0')  # 启动运行端口接收服务
        server = pywsgi.WSGIServer(('0.0.0.0', 1314), http)
        server.serve_forever()


class data_Thread(QThread):
    _signal = pyqtSignal(object)  # 定义信号类型为整型

    def __init__(self):
        super(data_Thread, self).__init__()
        self.run_flg = False

    def run(self):
        while True:
            if self.run_flg:
                message_list = update_userlist()
                self._signal.emit(message_list)  # 发射信号，把出错数据发送到列表窗口
                time.sleep(20)


def start_collectdata():
    if thread_data.run_flg == False:
        thread_data.run_flg = True
        thread_data.start()
        ui.pushButton.setText("暂停获取")
        ui.textEdit_2.append('开始获取操作。。。。。。')
    else:
        thread_data.run_flg = not (thread_data.run_flg)
        ui.pushButton.setText("启动获取")
        ui.textEdit_2.append('暂停获取。。。。。。')


def update_oklist(ip, name, username):
    try:
        table = 'oklist'
        sql = "SELECT max(addtime) FROM %s WHERE name='%s' " % (table, name)
        db_message = db_select(sql)

        w_list = session.get('http://%s:5000/w_list' % ip).content.decode('utf-8')  # 完成记录
        my_json = json.loads(w_list)
        data = my_json['data']
        for i in range(len(data) - 1, -1, -1):
            if int(data[i]['addtime']) > int(db_message[0][0]):
                s = data[i]['dow']
                num = s.find('Renamed final plot to ')
                if num:
                    print(len(s))
                    plot_to = s[num + len('Renamed final plot to '):len(s)]
                    print(plot_to)
                    num = plot_to.find('plot-k32-')
                    if num:
                        file = plot_to[num:len(plot_to)]
                        to_path = plot_to[0:num]
                        print('%s_%s' % (file, to_path))
                        # sql = 'INSERT INTO %s(name,addtime,endtime,path,file,to_path,username) ' \
                        #       'VALUES("%s","%s","%s","%s","%s","%s","%s")'\
                        #       %(table,name,data[i]['addtime'],data[i]['endtime'],
                        #         data[i]['path'],file,to_path,username)
                        # db_run(sql)
                        print(data[i])
    except:
        print('oklist 数据库操作出错')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = My_Gui()
    ui.setupUi(MainWindow)
    MainWindow.show()

    session = requests.session()

    thread_data = data_Thread()  # 开启线程
    # thread_data.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
    thread_data._signal.connect(signal_accept_data)
    thread_data.run_flg = False

    Thread_http = http_Thread()  # 开启线程
    Thread_http._signal.connect(signal_accept_data)
    Thread_http.run_flg = False
    Thread_http.start()

    ui.pushButton.clicked.connect(start_collectdata)
    ui.pushButton_2.clicked.connect(post_json)
    # data = session.get('http://192.168.77.191:5000/r_list')  # 进行中记录
    # print(data.content)
    # version = session.get('http://192.168.77.191:5000/version')  # 客户机软件版本
    # print(version.content)
    # e_config = session.post('http://192.168.77.191:5000/e_config')  # 修改客户机配置文件
    # print(e_config.content.decode('utf-8'))
    # io_info = session.get('http://192.168.77.191:5000/io_info')  # 存储介质资料
    # print(io_info.content)
    # info = session.get('http://192.168.77.191:5000/info')  # CPU,内存资料
    # print(info.content.decode('utf-8'))
    # w_list = session.get('http://192.168.77.191:5000/w_list')  # 完成记录
    # print(w_list.content)
    # update_userlist()
    # update_oklist('192.168.77.191', '1-5','216')

    sys.exit(app.exec_())
