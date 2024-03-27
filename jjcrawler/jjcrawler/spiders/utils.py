import requests
import re
import os
import logging
from rich.table import Table
from rich.panel import Panel
from rich import print

from .config import default_directory


def process_desc(desc_selector_list):
    if desc_selector_list == []:
        return
    desc_list = []
    first_line_break = False
    for selector in desc_selector_list:
        children = selector.xpath("child::node()")
        if children != []:
            desc_list += children.getall()
        else:
            desc_list += selector.getall()
    desc = []
    for line in desc_list:
        if line == "<br>":
            if first_line_break == False:
                first_line_break = True
            else:
                desc.append("")
        elif line[:3] == "<hr":
            continue
        else:
            desc.append(line)
            first_line_break = False
    return desc


def get_cover_path(directory, title):
    file_extension = ".jpg"
    return f"{directory}{title}{file_extension}"


def download_cover(directory, novel):
    print(f"下载 封面 中...")
    url = novel["cover_url"]
    if url:
        cover_path = get_cover_path(directory, novel["title"])
        response = requests.get(url)
        if response.status_code == 200:
            with open(cover_path, "wb") as file:
                for chunk in response:
                    file.write(chunk)


def get_chapter_id(url: str) -> str:
    ids = re.findall("\d+", url)
    if len(ids) == 1:
        chapter_id = None
    else:
        chapter_id = ids[1]
    return chapter_id


def make_directories(novel) -> str:
    if not os.path.exists(default_directory):
        os.mkdir(default_directory)
    directory = f"{default_directory}{novel['id'].rjust(7, '0')}-{novel['title']}\\"
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory


def get_novel_title(response):
    title = response.css("h1 span::text").get()
    if title:
        if "*" in title:
            new_title = ""
            asterisk = False
            for i in range(len(title)):
                if title[i] != "*":
                    if asterisk == True:
                        new_title += "[锁]"
                        asterisk = False
                    new_title += title[i]
                else:
                    if asterisk == False:
                        asterisk = True
            title = new_title
        return title.strip()


def num2chn(number_string):
    number = int(number_string)
    number_string = str(round(number, -2))[: len(number_string) - 2].rjust(2, "0")
    integer = number_string[:-2] or "0"
    decimal = number_string[-2:].rstrip("0")
    decimal = f".{decimal}" if decimal else ""
    return f"{integer}{decimal}万"


def get_second_row(novel):
    left = novel["author"]
    right = f"{num2chn(novel['word_count'])}·{novel['status']}"
    center = "".rjust(45 - len(left.encode("gbk")) - len(right.encode("gbk")), " ")
    return f"{left}{center}{right}"


def get_panel_content(novel):
    if novel["oneliner"]:
        return (
            f"[bold]{novel['title']}[/]\n"
            + f"[white]{get_second_row(novel)}\n"
            + f"{novel['genre']}\n"
            + f"{novel['oneliner']}[/]\n"
            + f":bookmark: [dark cyan]{novel['tags']}[/]"
        )
    else:
        return (
            f"[bold]{novel['title']}[/]\n"
            + f"[white]{novel['author']}\n"
            + f"{novel['genre']}[/]\n"
            + f"[deep_sky_blue1]{novel['error']}[/]"
        )


def get_tags(response, is_children_book=False):
    if is_children_book:
        tag_list = response.css("span span a::text").getall()
    else:
        tag_list = response.css("div.smallreadbody span a::text").getall()
    tags = ",".join(tag_list)
    if len(tags.encode("gbk")) > 42:
        tags = tags[:21] + "..."
    return tags


def get_word_count(response):
    text = response.css("li span::text")[8].get()[:-1]
    if text == "版权转化":
        text = response.css("li span::text")[7].get()[:-1]
    if text == "全文字数":
        text = response.css("li span::text")[9].get()[:-1]
    return text


def get_status(response):
    status = (
        response.css("ul.rightul li span font::text").get()
        or response.css("ul.rightul li span::text")[6].get()
    )
    if status == "文章进度：":
        status = response.css("ul.rightul li span::text")[7].get()
    return status


def get_author(response):
    return (
        response.css("h2 a span::text").get()
        or response.css("div.noveltitle span a::text").get()
    )


loggers = ["scrapy", "asyncio", "urllib3"]
# loggers = ["asyncio", "urllib3"]


def set_log_level():
    for logger in loggers:
        log = logging.getLogger(logger)
        log.setLevel(logging.WARNING)


def print_buttons():
    buttons = Table.grid(padding=0)
    buttons.add_column()
    buttons.add_column()
    buttons.add_row(
        Panel("[bold dark_cyan]:floppy_disk: 一键下载", border_style="dark_cyan"),
        Panel(":back: 返回"),
    )
    print(buttons)


def remove_reserved_characters(string):
    return re.sub(r'[<>:"/\\|?*]', "", string)


def get_file_name(chapter):
    title = chapter["title"]
    title = remove_reserved_characters(title)
    if chapter["id"] != None:
        file_name = f"第{chapter['id']}章-{title}"
    else:
        file_name = title
    return file_name


def get_heading(chapter):
    if chapter["id"] != None:
        heading = f"第{chapter['id']}章 {chapter['title']}"
    else:
        heading = chapter["title"]
    return heading


def format_body(body):
    body_list = []
    first_line_break = False
    second_line_break = False
    for line in body:
        line = line.strip()
        if isEmpty(line) or line[:4] == "<div" or line[:5] == "<span":
            continue
        elif line == "<br>":
            if second_line_break == False:
                if first_line_break == True:
                    second_line_break = True
                else:
                    first_line_break = True
        else:
            if second_line_break == True:
                body_list.append("")
            line = left_indent(line)
            body_list.append(line)
            first_line_break = False
            second_line_break = False
    return body_list


def isEmpty(line: str):
    if line == "":
        return True
    elif line == "[":
        return True
    elif line == "]":
        return True
    elif line == "支持手机扫描二维码阅读":
        return True
    elif line == "wap阅读点击：":
        return True
    elif line == "打开晋江App扫码即可阅读":
        return True
    else:
        return False


def left_indent(line):
    return "\u3000\u3000" + line
