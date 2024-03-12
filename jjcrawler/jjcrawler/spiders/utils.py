from urllib.request import urlretrieve
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


def get_cover_path(url, directory, title):
    file_extension = url.split(".")[-1]
    if len(file_extension) > 5:
        file_extension = "jpg"
    return f"{directory}{title}.{file_extension}"


def download_cover(directory, novel):
    url = novel["cover_url"]
    if url:
        cover_path = get_cover_path(url, directory, novel["title"])
        urlretrieve(url, cover_path)


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
