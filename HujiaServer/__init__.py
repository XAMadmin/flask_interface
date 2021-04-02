from flask import Flask
from config import config_map
import logging
from logging.handlers import RotatingFileHandler


def setup_log(config_name):
    """配置日志"""

    # 设置日志的记录等级
    logging.basicConfig(level=config_map[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("./logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)



def create_app(config_name):
    setup_log(config_name)
    app = Flask(__name__)
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)
    

    # 注册蓝图
    from . import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix = '/api/v1.0')
    return app