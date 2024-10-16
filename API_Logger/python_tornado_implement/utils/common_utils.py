"""通用utils
"""
import logging
import time
from datetime import datetime


def get_current_time_str():
    """获取当前时间字符串
    """
    return "{:%Y-%m-%d %H:%M:%S}".format(datetime.now())


func2time_map = {} # 函数名_extra_msg - 耗时毫秒统计，注意「耗时毫秒」是list，以防多次调用，最后可以打印func2time_map
def calculate_time(extra_msg=""):
    """
    将函数作为装饰器返回，用于计算函数执行时间并记录日志。
    
    Args:
        extra_msg (str): 附加信息，默认为 None。
    
    Returns:
        Callable[[Callable], Callable]: 返回一个带有额外功能的函数，该函数包含计算时间和记录日志的功能。
    """
    def decorator(func):
        """_summary_

        Args:
            func (_type_): _description_
        """
        def wrapper(*args, **kwargs):
            """_summary_

            Returns:
                _type_: _description_
            """
            start_time = time.time()
            result = func(*args, **kwargs)
            cost_time = (time.time() - start_time) * 1000
            logging.info("exec [{}] [{}] cost: {}ms".format(extra_msg, func.__name__, cost_time))
            save_key = "[func__{}]_[extra_msg__{}]".format(func.__name__, extra_msg if extra_msg else "None")
            if save_key not in func2time_map:
                func2time_map[save_key] = [cost_time]
            else:
                func2time_map[save_key].append(cost_time)
            return result
        return wrapper
    return decorator


def str2bool(v):
    """
    str to bool
    Returns:
        _type_: isMergeRawRecord
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 'y', '1', 'True'):
        return True
    else:
        return False