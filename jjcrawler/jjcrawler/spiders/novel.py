import scrapy

from .utils import process_desc, download_cover, get_chapter_id, make_directories
from .doc import create_desc_doc, create_chapter_doc


class NovelSpider(scrapy.Spider):
    name = "novel"

    def __init__(self, id=None, *args, **kwargs):
        if not id:
            print("usage: scrapy crawl book -a id=ID")
            print("error: the following argument is required: ID")

        super(NovelSpider, self).__init__(*args, **kwargs)

        self.allowed_domains = ["www.jjwxc.net"]
        self.start_urls = [f"https://www.jjwxc.net/onebook.php?novelid={id}"]

    def parse(self, response):
        novel = {}
        novel["title"] = response.css("h1 span::text").get()
        novel["cover_url"] = response.css("img.noveldefaultimage::attr(src)").get()
        novel["desc"] = process_desc(
            response.xpath('//*[@id="novelintro"]/node()').getall()
        )
        novel["tag_list"] = response.css("div.smallreadbody span a::text").getall()
        novel["keywords"] = response.css("span.bluetext::text").get()
        novel["oneliner"] = response.css("div.smallreadbody span::text")[2].get()
        novel["meaning"] = response.css("div.smallreadbody span::text")[3].get().strip()

        self.directory = make_directories(novel["title"])

        create_desc_doc(self.directory, novel)
        download_cover(self.directory, novel)

        chapters = response.css("span div a")
        for chapter in chapters:
            url = chapter.attrib["href"]
            yield response.follow(url, callback=self.parse_chapter)

    def parse_chapter(self, response):
        chapter = {}
        chapter["id"] = get_chapter_id(response.url)
        chapter["title"] = response.css("div.novelbody div div h2::text").get()
        chapter["body"] = response.xpath(
            "//div[@class='novelbody']/div/node()"
        ).getall()
        chapter["author_said"] = response.css("div.readsmall::text").getall()

        create_chapter_doc(self.directory, chapter)
