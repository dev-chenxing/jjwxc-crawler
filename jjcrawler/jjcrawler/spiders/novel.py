import scrapy

from .utils import (
    process_desc,
    download_cover,
    get_novel_title,
    get_chapter_id,
    make_directories,
    set_log_level,
)
from .novel_preview import novel_preview
from .doc import create_desc_doc, create_chapter_doc
from rich.panel import Panel


class NovelSpider(scrapy.Spider):
    name = "novel"

    def __init__(self, id=None, *args, **kwargs):
        set_log_level()
        super(NovelSpider, self).__init__(*args, **kwargs)

        self.allowed_domains = ["www.jjwxc.net"]
        self.start_urls = [f"https://www.jjwxc.net/onebook.php?novelid={id}"]
        self.id = str(id)
        self.parsed = False

    def parse(self, response):
        self.parsed = True
        download = novel_preview(self.id, response)
        if not download:
            return

        novel = self.get_novel_item(response)
        self.directory = make_directories(novel)
        if novel["tag_list"] != None:
            create_desc_doc(self.directory, novel)
            download_cover(self.directory, novel)

        chapters = response.css("span div a")
        if chapters == []:
            yield response.follow(response.url, callback=self.parse_chapter)
        else:
            for chapter in chapters:
                try:
                    url = chapter.attrib["href"]
                    yield response.follow(url, callback=self.parse_chapter)
                except:
                    continue

    def get_novel_item(self, response):
        novel = {}
        novel["id"] = self.id
        novel["title"] = get_novel_title(response)
        if novel["title"] == None:
            return
        novel["cover_url"] = response.css("img.noveldefaultimage::attr(src)").get()
        smallreadbody = response.css("div.smallreadbody span::text")
        if smallreadbody == []:
            novel["desc"] = response.css("div.smallreadbody::text").getall()
            (
                novel["tag_list"],
                novel["keywords"],
                novel["oneliner"],
                novel["meaning"],
            ) = (None, None, None, None)
        else:
            novel["desc"] = process_desc(response.xpath('//*[@id="novelintro"]/node()'))
            novel["tag_list"] = response.css("div.smallreadbody span a::text").getall()
            novel["keywords"] = response.css("span.bluetext::text").get()
            novel["oneliner"] = smallreadbody[2].get()
            novel["meaning"] = smallreadbody[3].get().strip()
        return novel

    def parse_chapter(self, response):
        chapter = {}
        chapter["id"] = get_chapter_id(response.url)
        chapter["title"] = response.css("div.novelbody div div h2::text").get()
        if chapter["title"] == None:
            return
        chapter["body"] = response.xpath(
            "//div[@class='novelbody']/div/node()"
        ).getall()
        chapter["author_said"] = process_desc(response.css("div.readsmall"))

        create_chapter_doc(self.directory, chapter)

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
