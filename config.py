# coding:utf-8
import logging


class MyConfig(object):

    """
    基础配置信息
    """
    SECRET_KEY = "XHSOI*Y9dfs9cshd9"
    # DB_URL = "" # 在配置文件中配置数据库连接地址
    DEBUG = True
    # 默认日志等级
    LOG_LEVEL = logging.DEBUG


class ProductConfig(MyConfig):
    """开发模式配置信息"""
    DEBUG = False
    LOG_LEVEL = logging.INFO


class DevelopConfig(MyConfig):
    """生产模式配置信息"""
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


config_map = {

    "product": ProductConfig,
    "develop": DevelopConfig
}
