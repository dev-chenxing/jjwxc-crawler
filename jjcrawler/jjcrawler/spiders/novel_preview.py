from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import scrapy
from scrapy.crawler import CrawlerProcess
from .novel import NovelSpider
import os

from .utils import (
    get_novel_title,
    get_panel_content,
    get_tags,
    get_word_count,
    get_status,
)

console = Console()


class NovelPreviewSpider(scrapy.Spider):
    name = "novel_preview"

    def __init__(self, id=None, *args, **kwargs):
        super(NovelPreviewSpider, self).__init__(*args, **kwargs)

        self.allowed_domains = ["www.jjwxc.net"]
        self.start_urls = [f"https://www.jjwxc.net/onebook.php?novelid={id}"]
        self.id = str(id)
        self.parsed = False

    def parse(self, response):
        self.parsed = True
        novel = self.get_novel_item(response)
        if novel == None:
            panel = Panel(
                "         该文已经删除或者全文存稿中",
                style="bold red",
                border_style="bright_white",
                width=48,
            )
            print(panel)
            return
        panel = Panel(
            get_panel_content(novel),
            style="dark_cyan",
            border_style="dark_cyan",
            width=48,
        )
        print(panel)
        buttons = Table.grid(padding=0)
        buttons.add_column()
        buttons.add_column()
        buttons.add_row(
            Panel(
                "[bold dark_cyan][1] :floppy_disk: 一键下载", border_style="dark_cyan"
            ),
            Panel("[2] :back: 返回"),
        )
        print(buttons)
        answer = Prompt.ask(
            "请选择一个操作",
            choices=["1", "2"],
            default="1",
            show_choices=False,
            show_default=False,
        )
        if answer == "1":
            os.system(f"scrapy crawl novel -a id={self.id} --loglevel WARNING")
            # process = CrawlerProcess()
            # process.crawl(NovelSpider, id=self.id)
            # process.start()

    def get_novel_item(self, response):
        novel = {}
        novel["id"] = self.id
        novel["title"] = get_novel_title(response)
        if novel["title"] == None:
            return
        smallreadbody = response.css("div.smallreadbody span::text")
        if smallreadbody == []:
            novel["tags"] = None
            novel["oneliner"] = None
            novel["error"] = "文案内容需作者填写身份信息后方能展示。"
        else:
            novel["tags"] = get_tags(response)
            novel["oneliner"] = smallreadbody[2].get().split("：")[1]
        novel["author"] = response.css("h2 a span::text").get()
        novel["genre"] = response.css("li span::text")[1].get().strip()
        novel["word_count"] = get_word_count(response)
        novel["status"] = get_status(response)
        return novel

    def close(self, spider):
        if not self.parsed:
            print(
                Panel(
                    "      非常抱歉，相关内容已被锁定或删除。",
                    style="bold red",
                    border_style="bright_white",
                    width=48,
                )
            )
