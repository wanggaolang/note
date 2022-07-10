# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from sys import version_info


import os
import time
import platform
from logging.handlers import TimedRotatingFileHandler


class SafeRotatingFileHandler(TimedRotatingFileHandler):
    """
    复写TimedRotatingFileHandler 解决多线程写日志切分时只有一个进程能顺利切换的问题
    """
    def __init__(self, filename, when='h', interval=1, backupCount=0, 
                 encoding=None, delay=False, utc=False):
        TimedRotatingFileHandler.__init__(self, 
                                          filename, when, interval,
                                          backupCount, encoding, delay, utc)
        self.delay = delay  # 2.7.5版本以下，FileHandler没有delay这个字段

    """
    Override doRollover
    lines commanded by "##" is changed by cc
    """
    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        if version_info.major == 3: # 仅在python3定义了rotation_filename
            dfn = self.rotation_filename(self.baseFilename + "." +
                                     time.strftime(self.suffix, timeTuple))
        else:
            dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)

        
        # 注释掉原来的逻辑
        # if os.path.exists(dfn):
        #     os.remove(dfn)
        # self.rotate(self.baseFilename, dfn)
            
        ### 重写开始，加文件锁切分。linux 文件锁，同os系统下 多进程锁
        if platform.system() != 'Windows':
            # fcntl锁的粒度是整个文件，别的进程不能对这个文件加锁
            fcntl = __import__("fcntl")
            f = open('logrename.lock', 'wb')
            # f = open(self.baseFilename, 'a')
            try:
                fcntl.flock(f, fcntl.LOCK_EX)   # 互斥锁
                # 如果不存在切分文件并且存在currentlog，重新命名
                if not os.path.exists(dfn) and os.path.exists(self.baseFilename):
                    os.rename(self.baseFilename, dfn)
                # 解锁
                fcntl.flock(f, fcntl.LOCK_UN)
            except:
                pass
            f.close()
        else:
            # 如果不存在切分文件并且存在currentlog，重新命名
            if not os.path.exists(dfn) and os.path.exists(self.baseFilename):
                os.rename(self.baseFilename, dfn)
        #### 重写结束
        
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        #If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt
