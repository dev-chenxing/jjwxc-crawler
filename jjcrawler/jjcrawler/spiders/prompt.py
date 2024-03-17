from rich.prompt import Prompt
import os


def prompt():
    novelid = Prompt.ask("[dark_cyan]  :mag: 请输入想要下载的作品的书号")
    if novelid:
        os.system(f"scrapy crawl novel_preview -a id={novelid} --loglevel WARNING")
