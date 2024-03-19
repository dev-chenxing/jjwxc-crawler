import requests
import re
import os

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


def get_tags(response):
    tags = ",".join(response.css("div.smallreadbody span a::text").getall())
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
