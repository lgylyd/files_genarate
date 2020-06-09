# coding:utf-8
import logging.handlers
from datetime import datetime
import sys
#from execute.public.utility import mkdir
#from execute.public.LogConfig import BASE_LOG
from pathlib import Path
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_LOG = {
    "level": 1,  # level: 1=debug,2=info,3=warning,4=error,5=critical
    "out_file_path": ROOT_DIR+"\\log",
    "use_handlers": [1,2],  # handler:1=file,2=stream,3=timedRotatingFile
    "file": {
        "encoding": "UTF-8"
    },
    "timed_rotating_file": {
        "filename": "time",
        "when": "D",  # when:'S'=Seconds,'M'=Minutes,'H'=Hours,
                      # 'D'=Days,'W0'-'W6'=Weekday (0=Monday),'midnight'=Roll over at midnight
        "encoding": "UTF-8"
    }
}

def mkdir(p):
    """
    功能说明：创建指定的目录
    :param p:
    :return:
    """
    try:
        path = Path(p)
        if not path.is_dir():
            path.mkdir()
    except Exception as e:
        print("指定路径不存在，创建报错，需要在异常中处理：" + str(e))
        os.makedirs(p)
    finally:
        return p

def today():
    now = datetime.now()
    return now.strftime('%Y%m%d_%H')

# 获取logger实例
logger = logging.getLogger("postman_sql")

# 创建日志目录
mkdir(BASE_LOG["out_file_path"])
# 文件日志
log_file = BASE_LOG["out_file_path"]+"\\"+today()+".log"

# 指定logger输出格式
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s line:%(lineno)d: %(message)s')

# 获取日志输出方式
use_handlers = BASE_LOG["use_handlers"]
for h in use_handlers:
    if h == 1:
        file = BASE_LOG["file"]
        file_handler = logging.FileHandler(filename=log_file, encoding=file["encoding"],mode='a')
        file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
        logger.addHandler(file_handler)  # 为logger添加的日志处理器
    if h == 2:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.formatter = formatter  # 也可以直接给formatter赋值
        logger.addHandler(console_handler)  # 为logger添加的日志处理器
    if h == 3:
        time_rotating = log_base["timed_rotating_file"]
        timed_rotating_handler = logging.handlers.TimedRotatingFileHandler(
            #改filename=Path(log_base["out_file_path"]) / f'{time_rotating["filename"]}.log',
            filename=time_rotating["filename"]+".log",
            when=time_rotating["when"],
            interval=1,  # interval 是指等待多少个单位when的时间后，Logger会自动重建文件，当然，这个文件的创建取决于filename+suffix
            backupCount=0,  # backupCount 是保留日志个数。默认的0是不会自动删除掉日志。若超过，则会从最先创建的开始删除。
            encoding=time_rotating["encoding"]
        )
        timed_rotating_handler.suffix = "%Y-%m-%d-%H%M.log"
        timed_rotating_handler.setFormatter(formatter)
        logger.addHandler(timed_rotating_handler)


# 指定日志的最低输出级别，默认为WARN级别:1=debug,2=info,3=warning,4=error,5=critical
# DEBUG，INFO，WARNING，ERROR，CRITICAL
level = BASE_LOG['level']
if level == 1:
    logger.setLevel(logging.DEBUG)
elif level == 2:
    logger.setLevel(logging.INFO)
elif level == 3:
    logger.setLevel(logging.WARNING)
elif level == 4:
    logger.setLevel(logging.ERROR)
elif level == 5:
    logger.setLevel(logging.CRITICAL)
else:
    logger.setLevel(logging.INFO)

if __name__ == '__main__':
    logger.info("test")