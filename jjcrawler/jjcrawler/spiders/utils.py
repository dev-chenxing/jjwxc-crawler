from urllib.request import urlretrieve
import re
import os

from .config import default_directory


def process_desc(description):
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


def get_cover_path(url, directory, title):
    file_extension = url.split(".")[-1]
    return f"{directory}{title}.{file_extension}"


def download_cover(directory, novel):
    cover_path = get_cover_path(novel["cover_url"], directory, novel["title"])
    urlretrieve(novel["cover_url"], cover_path)


def get_chapter_id(url: str) -> str:
    ids = re.findall("\d+", url)
    return ids[1]


def make_directories(title) -> str:
    if not os.path.exists(default_directory):
        os.mkdir(default_directory)
    directory = default_directory + title + "\\"
    if not os.path.exists(directory):
        os.mkdir(directory)
    print(directory)
    return directory
