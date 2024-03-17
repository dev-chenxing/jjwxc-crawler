from rich import print
from rich.panel import Panel
from jjcrawler.spiders.prompt import prompt


print(
    Panel(
        "            [bold]重生之我在绿江刮刮乐",
        style="dark_cyan",
        border_style="dark_cyan",
        width=48,
    )
)

prompt()
