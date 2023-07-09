# -*- coding: utf-8 -*-
import logging
import log
import os

if __name__ == '__main__':
    #测试Logger类
    logger = log.Logger('./logs/test_logger/app.log', 'debug', 'D', 5).logger
    logger.debug('debug')
    logger.info('info')
    logger.warning('警告')
    logger.error('报错')
    logger.critical('严重')

    #测试init_log方法
    file_name = os.path.basename(__file__).split(".")[0]
    log.init_log('./logs/test_logger/{}'.format(file_name), 'debug', 'D', 5)
    logging.debug('debug')
    logging.info('info')
    logging.warning('警告')
    logging.error('报错')
    logging.critical('严重')
