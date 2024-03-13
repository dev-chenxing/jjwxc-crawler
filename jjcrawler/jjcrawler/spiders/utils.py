import requests
import re
import os

from .config import default_directory


def process_desc(description):
    if description == []:
        return
    desc = []
    first_line_break = False
    second_line_break = False
    for line in description:
        if line == "<br>":
            if second_line_break == False:
                if first_line_break == True:
                    second_line_break = True
                else:
                    first_line_break = True
        else:
            if second_line_break == True:
                desc.append("")
            desc.append(line)
            first_line_break = False
            second_line_break = False
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
    print(directory)
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
    else:
        return
