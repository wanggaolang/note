"""
根据不同环境加载不同配置项
"""


import logging
import os
import importlib

ENV = {
    "dev": "dev",
    "test": "test",
    "online": "online"
}

def get_env():
    """获取当前运行环境，返回值为ENV其中一种

    Returns:
        ENV(str): _description_
    """
    env = os.environ.get('SERVER_ENV', ENV["dev"]).lower()
    if env not in ENV.values():
        env = ENV["dev"]
    return env


def load_settings():
    """根据环境加载配置
    """
    env = get_env()
    conf = importlib.import_module('config.env.config_{}'.format(env))
    return conf


load_env_settings = load_settings()
