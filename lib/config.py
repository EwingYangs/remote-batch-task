"""配置文件"""
# 线程池线程数量
ThreadPoolNum = 10

# 是否写日志
LogApp = True
AppLog = 'app.log'

# 服务器配置文件
Server = [
    {"host":"192.168.1.222", "port":"22", "username":"root", "password":"123456"},
    {"host":"192.168.10.10", "port":"22", "username":"root", "password":"123456"},
    {"host":"192.168.33.10", "port":"22", "username":"vagrant", "password":"vagrant"},
]