# coding=utf-8
from __future__ import print_function

LOG_INFO = 10
LOG_WARNING = 30
LOG_ERROR = 40

_level = LOG_WARNING


def log_config(lv):
    global _level
    _level = lv


def info(msg):
    if _level <= LOG_INFO:
        _print('INFO', msg)


def warning(msg):
    if _level <= LOG_WARNING:
        _print('WARNING', msg)


def error(msg):
    if _level <= LOG_ERROR:
        _print('ERROR', msg)


def message(msg):
    _print('MESSAGE', msg)


def _print(tag, msg):
    print('%-8s %s' % ('[%s]' % tag, msg))
