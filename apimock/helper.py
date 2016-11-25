#!/usr/bin/env python
# coding=utf-8
"""API Mock Helper.

Usage:
    api.mock [init | push | clean] [-d DIR] [-v | --verbose]
    api.mock (-h | --help)
    api.mock --version

Options:
    init          Generate default config files.
    push          Push configs to Android device.
    clean         Remove config files.
    -d DIR        The location of config files (default current directory).
    -v --verbose  Print more text.
    -h --help     Show this message.
    --version     Show version.

More information see:
  https://github.com/brucezz/APIMockHelper
  https://github.com/brucezz/APIMock

"""

from __future__ import print_function

import json

import os
import re
from device import get_device, get_devices
from docopt import docopt
from prettytable import PrettyTable
from util import LOG_INFO, LOG_WARNING, info, warning, message, error, log_config


class PushHelper(object):
    VERSION = '1.0.3'

    CONFIG_MOCK_DIR_NAME = 'mock'

    CONFIG_FILE_NAME = 'config.json'

    KEY_REMOTE = 'remote'
    KEY_BASE = 'base'
    KEY_DELAY = 'delay'
    KEY_ROUTE = 'route'

    DEFAULT_CONFIG = {
        KEY_REMOTE: "/storage/emulated/0/APIMock",
        KEY_BASE: "http://api.yourhost.com",
        KEY_DELAY: 500,
        KEY_ROUTE: {
        }
    }

    CONFIG_PATH = os.curdir
    CONFIG_FILE = ''
    CONFIG_MOCK_DIR = ''

    def __init__(self, config_path=None, verbose=False):
        """
        初始化
        :param config_path: 配置文件所在目录
        :return:
        """
        if config_path:
            self.CONFIG_PATH = config_path

        self.CONFIG_PATH = os.path.abspath(self.CONFIG_PATH)
        self.CONFIG_FILE, self.CONFIG_MOCK_DIR = PushHelper._build_paths(
            self.CONFIG_PATH)

        log_config(LOG_INFO if verbose else LOG_WARNING)

    @classmethod
    def _build_paths(cls, target):
        """
        构建配置文件的路径
        :param target:配置文件所在目录
        :return: (config_file, config_mock_dir) tuple 配置文件和 mock 数据文件夹的路径
        """
        config_file = os.path.join(target, cls.CONFIG_FILE_NAME)
        config_mock_dir = os.path.join(target, cls.CONFIG_MOCK_DIR_NAME)
        return config_file, config_mock_dir

    def init(self):
        """
        初始化创建配置文件和数据文件夹
        """
        info('Generating config files at %s' % self.CONFIG_PATH)

        if os.path.exists(self.CONFIG_FILE):
            warning('Found %s exist.' % self.CONFIG_FILE_NAME)
        else:
            info('Create %s.' % self.CONFIG_FILE)
            with open(self.CONFIG_FILE, 'w') as fp:
                fp.write(json.dumps(self.DEFAULT_CONFIG,
                                    indent=4, sort_keys=True))

        if os.path.exists(self.CONFIG_MOCK_DIR):
            warning('Found directory %s exist.' % self.CONFIG_MOCK_DIR_NAME)
        else:
            info('Create directory %s.' % self.CONFIG_MOCK_DIR_NAME)
            os.makedirs(self.CONFIG_MOCK_DIR)

        message('Init completed.')

    def _check_config(self):
        """
        校验配置文件
        :return: 设备上的推送位置
        """
        config = self._check_json_file(self.CONFIG_FILE)
        if config is None:
            return

        # 检查 remote 字段
        remote = config.get(self.KEY_REMOTE)

        if not remote:
            error('Invalid value of "%s" in %s' % (self.KEY_REMOTE, self.CONFIG_FILE_NAME))
            return

        route = config.get(self.KEY_ROUTE)

        if route:
            for regex, data in route.iteritems():
                # check regex
                if not self._check_regex(regex):
                    return

                # check mock data JSON format
                mock_data = os.path.join(self.CONFIG_PATH, data)
                if self._check_json_file(mock_data) is None:
                    return

        return remote

    @staticmethod
    def _check_json_file(path):
        """
        检查 JSON 文件的格式
        :param path: 文件路径
        :return: JSON 格式合法, 返回 True
        """
        if not PushHelper._check_file_exist(path):
            return

        try:
            with open(path) as fp:
                return json.loads(fp.read())
        except ValueError:
            error('Invalid JSON format: %s' % path)

    @staticmethod
    def _check_file_exist(path):
        """
        检查文件是否存在
        :param path: 文件路径
        :return: 如果文件存在, 返回 True
        """
        if os.path.exists(path):
            return True
        else:
            error("File not found: %s" % path)

    @staticmethod
    def _check_regex(regex):
        """
        检查正则表达式的格式
        :param regex: 正则表达式
        :return: 如果正则表达式编译通过, 返回 True
        """
        try:
            return re.compile(regex)
        except:
            error('Invalid regex: %s' % regex)

    @staticmethod
    def _select_device():
        """
        在在线设备多余 1 台时, 通过终端输入来选取.
        仅有 1 台在线时, 自动选取.
        """
        devices = map(get_device, get_devices())
        if not devices:
            error('No devices.')
        elif len(devices) == 1:
            return devices[0]
        else:
            print('Found more than one devices:')

            PushHelper._draw_table(devices)

            select = raw_input('\nEnter the index of devices(0 ~ %d): ' % (len(devices) - 1))
            try:
                select = int(select)
                if 0 <= select < len(devices):
                    return devices[select]
            except:
                pass
            error('Invalid input!')

    @staticmethod
    def _draw_table(devices):
        """
        绘制展示多设备信息的表格
        :param devices:多个 Android 设备
        """

        table = PrettyTable(['Index', 'Serial', 'Model'])
        for idx, device in enumerate(devices):
            table.add_row([idx, device.serial, device.model])
        print(table)

    def _push(self, device, remote):
        """
        推送配置信息到设备上
        :param device: 目标设备
        :param remote: 设备上的位置
        """
        info('Pushing configs to [%s] %s ...' % (device.serial, remote))

        remote_config_file, remote_mock_dir = self._build_paths(remote)

        device.push(self.CONFIG_FILE, remote_config_file)
        device.push(self.CONFIG_MOCK_DIR, remote_mock_dir)

    def push(self):
        """
        安装配置文件命令
        """
        remote = self._check_config()

        if not remote:
            return

        device = self._select_device()

        if not device:
            return

        self._push(device, remote)

        message('Push completed!')

    def clean(self):

        if os.path.exists(self.CONFIG_FILE):
            warning('Removing %s' % self.CONFIG_FILE)
            os.remove(self.CONFIG_FILE)
        if os.path.exists(self.CONFIG_MOCK_DIR):
            warning('Removing directory %s' % self.CONFIG_MOCK_DIR)
            os.removedirs(self.CONFIG_MOCK_DIR)
        message('Clean complete.')

    @classmethod
    def process_args(cls):
        args = docopt(__doc__, version='API Mock Helper version %s' % cls.VERSION)
        helper = cls(args['-d'], args['--verbose'])
        if args['init']:
            helper.init()
        elif args['push']:
            helper.push()
        elif args['clean']:
            helper.clean()


def main():
    PushHelper.process_args()


if __name__ == '__main__':
    main()
