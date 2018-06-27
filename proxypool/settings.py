# Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'mx_proxy'

# Tester
INITIAL_SCORE = 10
MAX_SCORE = 100
MIN_SCORE = 0
TEST_URL = 'http://www.baidu.com/'
# 批量测试大小
TEST_BATCH_SIZE = 50
# 测试通过的状态：200，302（重定向）
VALID_STATUS = [200, 302]

# Api
API_HOST = 'localhost'
API_PORT = 8000

# 管理类
ENABLE_CRAWL = True
ENABLE_TEST = True
ENABLE_API = True
