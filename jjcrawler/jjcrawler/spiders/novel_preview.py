from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table
import scrapy

from .utils import (
    get_novel_title,
    get_panel_content,
    get_tags,
    get_word_count,
    get_status,
    get_author,
)

console = Console()


def novel_preview(id, response):
    novel = get_novel_item(id, response)
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
        Panel("[bold dark_cyan] :floppy_disk: 一键下载", border_style="dark_cyan"),
        Panel(" :back: 返回"),
    )
    print(buttons)
    answer = Confirm.ask("是否一键下载？")
    if answer == "y":
        return True


def get_novel_item(id, response):
    novel = {}
    novel["id"] = id
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
    novel["author"] = get_author(response)
    novel["genre"] = response.css("li span::text")[1].get().strip()
    novel["word_count"] = get_word_count(response)
    novel["status"] = get_status(response)
    return novel
