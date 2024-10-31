import re
from scrapy.http import Response
import scrapy
from .utils import set_log_level, get_chapter_id, get_novel_title, make_directories
from .txt import create_chapter_txt


class NovelListSpider(scrapy.Spider):
    name = "novellist"

    def __init__(self, xx, bq, sd=None, *args, **kwargs):
        set_log_level()
        super(NovelListSpider, self).__init__(*args, **kwargs)

        self.allowed_domains = ["www.jjwxc.net"]
        sd_text = "&".join(
            [f"sd{x}={x}" for x in sd.split(",")]) + "&" if sd else ""
        self.start_urls = [
            f"https://www.jjwxc.net/bookbase.php?xx{xx}={xx}&bq={bq}&{sd_text}page={i}" for i in range(1, 11)]

    def parse(self, response: Response):
        novel_list = response.css("tr")
        novel_list.pop(0)
        for novel in novel_list:
            href = novel.css("td a")[1].attrib["href"]
            url = f"https://www.jjwxc.net/{href}"
            yield response.follow(url, callback=self.parse_novel)

    def parse_novel(self, response: Response):
        novel = self.get_novel_item(response)
        directory = make_directories(novel)

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

    def get_novel_item(self, response):
        novel = {}
        novel["id"] = re.findall(r"\d+", response.url)[0]
        novel["title"] = get_novel_title(response)
        if novel["title"] == None:
            return
        page_title = response.css("title::text").get()
        if re.findall("小树苗", page_title) != []:
            return
        smallreadbody = response.css("div.smallreadbody span::text")
        if smallreadbody == []:
            novel["desc"] = response.css("div.smallreadbody::text").getall()
            (
                novel["tag_list"],
                novel["oneliner"],
                novel["meaning"],
            ) = (None, None, None)
        else:
            novel["tag_list"] = response.css(
                "div.smallreadbody span a::text").getall()
            novel["oneliner"] = smallreadbody[-2].get()
            novel["meaning"] = smallreadbody[-1].get().strip()
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
        create_chapter_txt(
            response.meta["directory"], response.meta["title"], chapter)
