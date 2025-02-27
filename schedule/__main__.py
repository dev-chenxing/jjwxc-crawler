import os
import schedule
import time

start_index = 349615


def job():
    global start_index
    os.system(command=f"scrapy crawl novels -a start={start_index}")
    start_index += 1001


schedule.every().seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
