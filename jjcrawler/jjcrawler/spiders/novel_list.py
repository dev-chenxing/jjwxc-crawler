import re
import urllib.parse
from scrapy.http import Response
import scrapy
import urllib
from .utils import process_desc, set_log_level, get_chapter_id, get_novel_title, make_directories
from .txt import create_chapter_txt, create_desc_txt

orientation_map = {
    "1": "言情",
    "2": "纯爱",
    "3": "百合",
    "5": "无CP",
    "6": "多元",
}


class NovelListSpider(scrapy.Spider):
    name = "novellist"

    def __init__(self, xx, yc=None, title: str = None, sd=None, mainview=None, bq=-1, *args, **kwargs):
        set_log_level()
        super(NovelListSpider, self).__init__(*args, **kwargs)

        if title:
            self.kw = title
            self.xx = orientation_map[xx]
            self.allowed_domains = ["m.jjwxc.net"]
            kw = urllib.parse.urlencode({"kw": title}, encoding="gb18030")
            self.start_urls = [
                f"https://m.jjwxc.net/search/index/page/{i}?{kw}" for i in range(1, 10)]
            self.mobile_pages = True
        else:
            self.allowed_domains = ["www.jjwxc.net"]
            sd_text = "&".join(
                [f"sd{x}={x}" for x in sd.split(",")]) + "&" if sd else ""
            self.start_urls = [
                f"https://www.jjwxc.net/bookbase.php?yc={yc}&xx{xx}={xx}&mainview={mainview}&bq={bq}&{sd_text}page={i}" for i in range(1, 11)]

    def parse(self, response: Response):
        if self.mobile_pages:
            novel_list = response.css("li")
            novel_list.pop(-1)
            for novel_li in novel_list:
                novel = novel_li.css("a")[0]
                title = "".join(novel.css("::text").getall())
                if re.match(self.kw, title):
                    href = novel.attrib["href"]
                    url = f"https://m.jjwxc.net/{href}"
                    yield response.follow(url, callback=self.parse_novel)
        else:
            novel_list = response.css("tr")
            novel_list.pop(0)
            for novel in novel_list:
                href = novel.css("td a")[1].attrib["href"]
                url = f"https://www.jjwxc.net/{href}"
                yield response.follow(url, callback=self.parse_novel)

    def parse_novel(self, response: Response):
        novel = self.get_novel_item(response)

        if self.mobile_pages:
            if novel:
                print(novel["id"], novel["title"], novel["full_genre"])
        else:
            directory = make_directories(novel)
            create_desc_txt(directory, novel)

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
        novel["title"] = get_novel_title(
            response, is_mobile_pages=self.mobile_pages)
        if novel["title"] == None:
            return
        if self.mobile_pages:
            novel["id"] = re.findall(r"\d+", response.url)[1]
            novel["full_genre"] = response.css("#left li")[2].css(
                "::text").get().split("：")[1].strip()
            if re.search(self.xx, novel["full_genre"]):
                return novel
        else:
            novel["id"] = re.findall(r"\d+", response.url)[0]
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
