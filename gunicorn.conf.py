from gevent import monkey
import multiprocessing
monkey.patch_all()
bind = "0.0.0.0:8002"
# 启动的进程数
workers = multiprocessing.cpu_count()
worker_class = 'gevent'