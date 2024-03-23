from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.prompt import Confirm
import re

from .utils import (
    get_novel_title,
    get_panel_content,
    get_tags,
    get_word_count,
    get_status,
    get_author,
    print_buttons,
)

console = Console()


def novel_preview(id, response):
    novel, is_children_book = get_novel_item(id, response)
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
    if novel["tags"] != None:
        if is_children_book:
            print(
                Panel(
                    "         暂不支持下载小树苗文学作品",
                    style="bold light_sea_green",
                    border_style="light_cyan1",
                    width=48,
                )
            )
        else:
            print_buttons()
            answer = Confirm.ask("是否一键下载？")
            return answer


def get_novel_item(id, response):
    novel = {}
    novel["id"] = id
    novel["title"] = get_novel_title(response)
    if novel["title"] == None:
        return None, False
    page_title = response.css("title::text").get()
    if re.findall("小树苗", page_title) != []:
        return get_children_novel_item(id, novel["title"], response), True
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
    return novel, False


def get_children_novel_item(id, title, response):
    novel = {}
    novel["id"] = id
    novel["title"] = title
    novel["tags"] = get_tags(response, True)
    novel["author"] = get_author(response)
    novel_meta = response.css("div.novelmeta_item_div span::text")
    novel["oneliner"] = novel_meta[-3].get()
    novel["genre"] = novel_meta[3].get()
    novel["word_count"] = novel_meta[1].get()[:-1]
    novel["status"] = (
        novel_meta[5].get().strip()
        or response.css("div.novelmeta_item_div span font::text").get()
    )
    return novel
