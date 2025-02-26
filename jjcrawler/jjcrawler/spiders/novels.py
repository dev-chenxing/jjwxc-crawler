import re

from .txt import create_chapter_txt, create_desc_txt
from .utils import get_chapter_id, get_novel_title, make_directories, process_desc, set_log_level, reset, green, dark_gray
import scrapy
from requests import Response
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="scrapy-novels.log",
                    encoding='utf-8', level=logging.DEBUG)


def log_success(text: str):
    logger.info(green+text+reset)


def log_failure(text: str):
    logger.info(dark_gray+text+reset)


class NovelsSpider(scrapy.Spider):
    name = "novels"

    def __init__(self, start: int, end: int = None, *args, **kwargs):
        set_log_level()
        super(NovelsSpider, self).__init__(*args, **kwargs)

        start = int(start)
        end = int(end) if end else start + 1000
        self.allowed_domains = ["www.jjwxc.net"]
        self.start_urls = [
            f"https://www.jjwxc.net/onebook.php?novelid={i}" for i in range(start, end + 1)]
        logger.info(f"Scraping novels, ID starting from {start} to {end}...")

    def parse(self, response: Response):
        novel, novel_id = self.get_novel_item(response)
        if not novel:
            log_failure(f"{novel_id} - no access - skipped")
            return

        if 'xx' not in novel:
            log_failure(
                f"{novel['id']} - {novel['title']} 文章类型：{novel['genre']} - skipped")
            return
        elif novel['xx'] == '百合':
            pass
        elif novel['xx'] == '无CP':
            pass
        else:
            log_failure(
                f"{novel['id']} - {novel['title']} 文章类型：{novel['genre']} - skipped")
            return

        if novel['word_count'] < 20000:
            log_failure(
                f"{novel['id']} - {novel['title']} - 全文字数：{novel['word_count']} - skipped")
            return

        log_success(
            f"{green}{novel['id']} - {novel['title']} 文章类型：{novel['genre']} - downloading{reset}")
        directory = make_directories(novel)
        create_desc_txt(directory, novel, quiet=True)

        chapters = response.css("span div a")
        if chapters == []:
            response.follow(response.url, callback=self.parse_chapter, meta={
                "directory": directory})
        else:
            for chapter in chapters:
                try:
                    url = chapter.attrib["href"]
                    yield response.follow(url, callback=self.parse_chapter, meta={"title": novel["title"], "directory": directory})
                except:
                    continue

    def parse_chapter(self, response):
        chapter = {}
        chapter["id"] = get_chapter_id(response.url)
        chapter["title"] = response.css("div.novelbody div div h2::text").get()
        if chapter["title"] == None:
            return
        chapter["body"] = response.xpath(
            "//div[@class='novelbody']/div/node()"
        ).getall()
        create_chapter_txt(
            response.meta["directory"], response.meta["title"], chapter, quiet=True)

    def get_novel_item(self, response):
        novel = {}
        novel["id"] = re.findall(r"\d+", response.url)[0]
        novel["title"] = get_novel_title(
            response, is_mobile_pages=False)
        if novel["title"] == None:
            return None, novel["id"]
        novel["genre"] = response.css(".rightul span::text")[1].get().strip()
        genre = novel["genre"].split("-")
        if len(genre) == 1:  # 文章类型： 随笔
            return None, novel["id"]
        elif len(genre) == 4:
            novel["yc"], novel["xx"], novel["sd"], novel["lx"] = genre
        novel["word_count"] = int(response.xpath(
            "//span[@itemprop='wordCount']/text()").get()[:-1])

        page_title = response.css("title::text").get()
        if re.findall("小树苗", page_title) != []:
            return
        smallreadbody = response.css("div.smallreadbody span::text")
        if smallreadbody == []:
            novel["desc"] = response.css(
                "div.smallreadbody::text").getall()
            (
                novel["tag_list"],
                novel["oneliner"],
                novel["meaning"],
            ) = (None, None, None)
        else:
            novel["desc"] = process_desc(
                response.xpath('//*[@id="novelintro"]/node()'))
            novel["tag_list"] = response.css(
                "div.smallreadbody span a::text").getall()
            novel["oneliner"] = smallreadbody[-2].get()
            novel["meaning"] = smallreadbody[-1].get().strip()
        return novel, novel["id"]
