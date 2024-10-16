"""用于将调用日志推送至服务器
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../etc/py_log_util'))
import traceback
import requests
import json
import time
import config.env.load_env as load_env
import logging
import tornado.web
import utils.common_utils as common_utils

class LogToServer(object):
    """用于tornado每个接口进行持有，最后统一调用该类的save方法进行日志上传

    Args:
        object (_type_): _description_
    """
    def __init__(self, interface_name, need_log=None):
        assert isinstance(need_log, (list, type(None)))
        self.required_log = ["interface_name", "access_time", "request_url"] # todo： 强制校验这些参数是否为空
        if need_log is not None:
            self.required_log += need_log
        self.log_dict = {} # 存储所有待上传的日志
        self.log_dict["interface_name"] = interface_name
        self.call_init_log_saver = False
        self.call_log_data_and_status = False

    def save(self):
        """_summary_
        """
        if load_env.load_env_settings.NEED_LOG_TO_SERVER is False:
            logging.info("NEED_LOG_TO_SERVER is False, skip log to server")
            return
        # 检查响应
        insert_log_url = load_env.load_env_settings.INSERT_LOG_URL
        try:
            json_data = common_utils.process_dict(self.log_dict)
            response = requests.post(insert_log_url,
                                     json=json_data, timeout=5)
            if response.status_code != 200:
                logging.error('log save failed, status code: {}, requset url: {}, log_dict data: {}, response: {}'.
                              format(response.status_code, insert_log_url, json_data, response.text))
        except Exception as err:
            logging.error('log save failed, requset url: {}, log_dict data: {}, reason: {}, trackback: {}'.format(
                insert_log_url, self.log_dict, err, traceback.format_exc()))

class BaseRequestHandler(tornado.web.RequestHandler):
    """对RequestHandler的封装
    Args:
        RequestHandler (_type_): _description_
    """
    def base_get_arguments(self, required_param_names=None, optional_param_names=None):
        """获取输入的必填参数和可选参数的值，返回为2个数组，第1个是必填参数里未填入值的key，第2个是输入的所有参数与值的map，
            若未获取到某参数值，则该值为None

        Args:
            required_param_names (str list): _description_
            optional_argument_names (str list): _description_

        Returns:
            tuple composed of 2 list: ([miss required argument names], [all input key-value map])
        """
        required_param_names = list(set(required_param_names)) if required_param_names is not None else []
        optional_param_names = list(optional_param_names) if optional_param_names is not None else []
        missed_required_params = []
        acl_all_keys = self.request.arguments.keys()
        for param_name in required_param_names:
            if param_name not in acl_all_keys:
                missed_required_params.append(param_name)

        uniq_argument_names = list(set(required_param_names) | set(optional_param_names)) # 去重
        all_input_key_value_map = {}
        for param_name in uniq_argument_names:
            all_input_key_value_map[param_name] = self.get_argument(param_name, None)
        return missed_required_params, all_input_key_value_map

    def add_log_wrapper(self, interface_name, need_log=None):
        """_summary_
        """
        log_saver = LogToServer(interface_name, need_log)
        def wrapper(func):
            def wrapper_internal(this, *args, **kwargs):
                """_summary_
                """
                this.init_log_to_server(log_saver)
                res = func(this, log_saver)
                this.flush()
                if not isinstance(log_saver, LogToServer):
                    raise Exception("log_saver is not LogToServer")
                if log_saver.call_init_log_saver is not True:
                    raise Exception("log_saver.init_log_saver is not called in func: {}, interface_name: {}".format(
                        func.__name__, interface_name))
                if log_saver.call_log_data_and_status is not True:
                    raise Exception("log_saver.log_data_and_status is not called in func: {}, interface_name: {}".format(
                        func.__name__, interface_name))
                log_saver.save()
                return res
            return wrapper_internal
        return wrapper

    def on_finish(self):
        common_utils.func2time_map = {}

    def set_headers(self):
        """设置允许跨域header
        """
        if self.request.headers.get('If-None-Match'): #防止返回304
            del self.request.headers['If-None-Match']
        self.set_header("Access-Control-Allow-Origin", self.request.headers.get("Origin", "http://localhost:8999"))
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("MATRIX_INSTANCE_ID", os.getenv('MATRIX_INSTANCE_ID', ""))

    def options(self):
        """处理 OPTIONS 请求，设置返回允许的请求方法和请求头等
        """
        self.set_headers()
        self.set_status(204)  # No Content
        self.finish()

    @common_utils.calculate_time()
    def init_log_to_server(self, server_logger):
        """_summary_
        """
        
        # log client request info
        server_logger.log_dict["access_time"] = common_utils.get_current_time_str()
        server_logger.log_dict["request_url"] = self.request.uri
        server_logger.log_dict["client_ip"] = self.request.remote_ip
        server_logger.log_dict["request_method"] = self.request.method
        server_logger.log_dict["request_header"] = str(json.dumps(dict(self.request.headers)))
        server_logger.log_dict["request_body"] = self.request.body
        server_logger.log_dict["request_body_size"] = len(self.request.body)
        ##### need custom request_identifier
        ##### need custom request_user
        ##### need custom client_environment

        # 服务端相关信息
        server_logger.log_dict["server_environment"] = load_env.get_env()
        server_logger.log_dict["service_instance_id"] = os.getenv("MATRIX_INSTANCE_ID", "")
        server_logger.log_dict["server_ip"] = self.request.host

        # log_source
        server_logger.log_dict["log_source"] = "server"

        ##### need custom reserved_field_1
        ##### need custom reserved_field_2
        server_logger.call_init_log_saver = True

    def log_data_and_status(self, server_logger, status, response_size=None, data=None):
        """_summary_
        """
        assert isinstance(server_logger, LogToServer)
        if not server_logger.call_init_log_saver:
            raise Exception("do not call call_init_log_saver before log_data_and_status in class: {}".format(
                self.__class__.__name__))
        server_logger.log_dict["response_time"] = common_utils.get_current_time_str()
        server_logger.log_dict["interface_duration"] = int(self.request.request_time() * 1000)
        if response_size is not None:
            server_logger.log_dict["response_size"] = response_size
        if data is not None:
            server_logger.log_dict["response_data"] = data
        if not (isinstance(status, int) and 0 <= status < 600):
            raise Exception("status must be an integer in range [0, 599]")
        server_logger.log_dict["response_status"] = status
        server_logger.call_log_data_and_status = True

class YourHandler(BaseRequestHandler):
    @add_log_wrapper(self)
    def get(self):
        required_params = ["required_param_1", "required_param_2"]  # 必填参数
        optional_params = ["optional_param_1", "optional_param_2"]  # 可选参数
        missed_required_params, all_input_key_value_map = self.base_get_arguments(required_params, optional_params)
        if missed_required_params:
            error_response = {
                "errno": 1,
                "msg": "Missing parameters: {}".format(", ".join(missed_required_params)),
            }
            self.write(json.dumps(error_response))
        else:
            # 执行你的逻辑，这里只是一个示例
            response_data = {
                "status": "Success",
                "data": "Your response data here",
                "all_input_key_value_map": all_input_key_value_map,
            }
            self.write(json.dumps(response_data))

def make_app():
    return tornado.web.Application([
        (r"/your_endpoint", YourHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)  # 你可以更改端口号
    tornado.ioloop.IOLoop.current().start()