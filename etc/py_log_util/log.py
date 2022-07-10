#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from safe_rotating_file_handler import SafeRotatingFileHandler

__inited_log_set = set()

verbose = '%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s'

simple = '[%(asctime)s] - [%(funcName)s:%(lineno)s] - %(message)s'

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFALT_LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(CURRENT_DIR)), 'log')
# 日志级别关系映射
level_relations = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

def init_log(log_path, level=logging.INFO, when="midnight", backup=15, _format=None, date_fmt=None):
    """
    init_log - initialize log module
    Args:
      log_path      - Log file path prefix.
                      Log data will go to two files: log_path.log and log_path.log.wf
                      Any non-exist parent directories will be created automatically
      level         - msg above the level will be displayed
                      DEBUG < INFO < WARNING < ERROR < CRITICAL
                      the default value is logging.INFO
      when          - how to split the log file by time interval
                      'S' : Seconds
                      'M' : Minutes
                      'H' : Hours
                      'D' : Days
                      'W' : Week day
                      'midnight' : midnight
                      default value: 'midnight'
      _format        - format of the log
                      default format:
                      %(levelname)s: %(asctime)s: %(filename)s:%(lineno)d %(threadName)s * %(message)s
                      INFO: 12-09 18:02:42: log_conf.py:40 MainThread * HELLO WORLD
      backup        - how many backup file to keep
                      default value: 14
      datefmt        - date format


    Raises:
        OSError: fail to create log directories
        IOError: fail to open log file
    """
    if _format is None:
        _format = verbose

    if log_path in __inited_log_set:
        return

    log_dir = os.path.dirname(log_path)
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    formatter = logging.Formatter(_format, date_fmt)
    logger = logging.getLogger(name=log_path)
    logger.setLevel(level_relations.get(level))
    logging.root = logger
    __inited_log_set.add(log_path)

    # handler = logging.handlers.SafeRotatingFileHandler(log_path + '.log',
    #                                                     when=when,
    #                                                     backupCount=backup)
    handler = SafeRotatingFileHandler(log_path + '.log', when=when, backupCount=backup)
    handler.setLevel(level_relations.get(level))
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # handler = SafeRotatingFileHandler(log_path + '.log.wf', when=when, backupCount=backup)
    # handler.setLevel(level_relations["warning"])
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)

    # stream logger
    handler = logging.StreamHandler()
    handler.setLevel(level_relations.get(level))
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class Logger(object):
    '''
    init_log - initialize log module
    Args:
      log_path      - Log file path prefix.
                      Log data will go to two files: log_path.log and log_path.log.wf
                      Any non-exist parent directories will be created automatically
      level         - msg above the level will be displayed
                      debug < info < warning < error < critical
                      the default value is logging.INFO
      when          - how to split the log file by time interval
                      'S' : Seconds
                      'M' : Minutes
                      'H' : Hours
                      'D' : Days
                      'W' : Week day
                      default value: 'D'
      fmt            - format of the log
                      default format:
                      %(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s
                      DEBUG: 2021-10-21 23:25:50,251: log.py:80 * 4480687552 HELLO WORLD
      backup        - how many backup file to keep
                      default value: 7
    Raises:
        OSError: fail to create log directories
        IOError: fail to open log file
    '''
    def __init__(self,
                 filename,
                 level='info',
                 when='D',
                 back_count=7,
                 fmt='%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s'):
        f_dir, f_name = os.path.split(filename)
        if not os.path.exists(f_dir):
            os.makedirs(f_dir)
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        # 往文件里写入指定间隔时间自动分割文件的Handler
        th = SafeRotatingFileHandler(filename=filename, when=when, backupCount=back_count)
                                               #encoding='utf-8')#加上这个后中文日志需为xxx.info(u'中文') 
        # 实例化SafeRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时
        # D 天
        # 'W0'-'W6' 每星期（interval=0时代表星期一：W0）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)
