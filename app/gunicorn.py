

# nohup gunicorn -c gunicorn.py run:app &


# 是否开启debug模式
debug = True
# 访问地址
bind = "0.0.0.0:5115"
# 工作进程数
workers = 2
# 工作线程数
threads = 2
# 超时时间
timeout = 600
# 输出日志级别
loglevel = 'debug'
# 存放日志路径
pidfile = "log/gunicorn.pid"
# 存放日志路径
accesslog = "log/access.log"
# 存放日志路径
errorlog = "log/debug.log"
# gunicorn + apscheduler场景下，解决多worker运行定时任务重复执行的问题
preload_app = True