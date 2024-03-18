from rich import print
from rich.panel import Panel
from rich.prompt import Prompt
import os


print(
    Panel(
        "            [bold]重生之我在绿江刮刮乐",
        style="dark_cyan",
        border_style="dark_cyan",
        width=48,
    )
)

novelid = Prompt.ask("[dark_cyan]  :mag: 请输入想要下载的作品的书号")
if novelid:
    os.system(f"scrapy crawl novel_preview -a id={novelid} --loglevel WARNING")
