# main.py
import schedule
import time
from utils import scheduled_task
import config
# 立即执行第一次任务
scheduled_task()
# 设置定时任务
schedule.every(config.FETCH_INTERVAL).minutes.do(scheduled_task)
# 启动定时任务
while True:
    schedule.run_pending()
    time.sleep(1)