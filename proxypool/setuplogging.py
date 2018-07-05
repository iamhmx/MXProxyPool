import os
import logging.config
import yaml
import logging

logger = logging.getLogger(__name__)


def setup_logging(default_path='logging.yaml', default_level=logging.INFO):
    """
    设置日志
    """
    if not os.getcwd().endswith('proxypool'):
        # 从run.py运行
        default_path = 'proxypool/' + default_path
    if os.path.exists(default_path):
        with open(default_path, 'rt') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
        logger.info('日志配置文件不存在，使用默认配置')
