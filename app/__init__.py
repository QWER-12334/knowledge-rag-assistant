#给整个文件的python包统一配置一个日志  getLogger是用来获取一个日志器
import logging
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - [%(levelname)s] %(name)s - %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
)