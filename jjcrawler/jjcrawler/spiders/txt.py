from pathlib import Path
from .utils import get_file_name, get_heading, format_body


def create_desc_txt(directory: Path, novel):
    print("下载 文案 中...")
    file_name = "文案"
    output_path = directory / f"{file_name}.txt"
    description_txt = open(output_path, "w", encoding="utf-8")

    for paragraph in novel["desc"]:
        description_txt.write(paragraph + "\n")

    tags = "内容标签： " + " ".join(novel["tag_list"])
    description_txt.write(tags + "\n")

    description_txt.write(novel["keywords"] + "\n")

    description_txt.write(novel["oneliner"] + "\n")

    description_txt.write(novel["meaning"] + "\n")

    description_txt.close()


def create_chapter_txt(directory: Path, chapter):
    file_name = get_file_name(chapter)
    print(f"下载 {file_name} 中...")

    output_path = directory / f"{file_name}.txt"
    chapter_txt = open(output_path, "w", encoding="utf-8")

    heading = get_heading(chapter)
    chapter_txt.write(heading + "\n\n")

    for paragraph in format_body(chapter["body"]):
        chapter_txt.write(paragraph + "\n")

    author_said = chapter["author_said"]
    if author_said:
        chapter_txt.write("\n")
        for author_said_p in author_said:
            chapter_txt.write(author_said_p + "\n")

    chapter_txt.close()
