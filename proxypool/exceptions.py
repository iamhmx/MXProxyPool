from proxypool.setuplogging import setup_logging
import logging

logger = logging.getLogger(__name__)


class EmptyException(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


if __name__ == '__main__':
    setup_logging()
    try:
        raise EmptyException('空的')
    except EmptyException as e:
        logger.error('代理池空异常', exc_info=True)
