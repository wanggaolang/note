#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from logging import handlers


class Logger(object):
    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

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
        #os.makedirs(f_dir, exist_ok=True)  #python3的创建目录 当前目录新建log文件夹,exist_ok=True表明创建目录的时候如果已经存在就不报错
        if not os.path.exists(f_dir): #python2的创建目录
            os.makedirs(f_dir)
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        # 往文件里写入指定间隔时间自动分割文件的Handler
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=back_count)
                                               #encoding='utf-8')#加上这个后中文日志需为xxx.info(u'中文') 
        # 实例化TimedRotatingFileHandler
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


# 测试
if __name__ == '__main__':
    logger = Logger('./logs/test_logger/app.log', 'debug', 'S', 5).logger
    logger.debug('debug')
    logger.info('info')
    logger.warning('警告')
    logger.error('报错')
    logger.critical('严重')

    # 单独记录error
    err_logger = Logger('./logs/test_logger/error.log', 'error', 'S', 3).logger
    err_logger.error(u'错误 error')
