#!/usr/bin/python
# -*- coding:utf-8 -*-


import logging

logging.basicConfig(format='%(asctime)s/[%(filename)s line:%(lineno)d] - %(levelname)s: %(message)s')
_logger = logging.getLogger()
_logger.setLevel(logging.INFO)

i = _logger.info
d = _logger.debug
w = _logger.warning
e = _logger.error


class Log:
    '''
    使用下面的方法会导致log的文件和行数始终是这个类
    '''

    @staticmethod
    def i(msg, *args, **kwargs):
        _logger.info(msg, *args, **kwargs)

    @staticmethod
    def d(msg, *args, **kwargs):
        _logger.debug(msg, *args, **kwargs)

    @staticmethod
    def w(msg, *args, **kwargs):
        _logger.warning(msg, *args, **kwargs)

    @staticmethod
    def e(msg, *args, **kwargs):
        _logger.error(msg, *args, **kwargs)


if __name__ == '__main__':
    pass
