from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn
from rich.table import Table
from rich import box

console = Console(width=64)

style = "dark_cyan on bright_white"

table = Table(show_footer=False)
table.add_column("请输入书号或书名", no_wrap=True)
table.add_column(":mag:", no_wrap=True, justify="center")

TABLE_DATA = [
    ["穿进百合游戏怎么办"],
    ["木云杉", "4.32万·连载"],
    ["原创-百合-近代现代-爱情"],
    ["穿进百合攻略游戏"],
    # ["[dark_cyan on bright_white]:bookmark: 穿越时空,轻松,脑洞,纸片人,万人迷,抽奖抽卡"],
]

for row in TABLE_DATA:
    table.add_row(*row)

for column in table.columns:
    column.header_style = "bright_white on dark_cyan"
    column.style = "grey11 on bright_white"

table.border_style = "grey93"
table.box = box.SIMPLE
table.pad_edge = True
table.show_edge = False
table.min_width = 46

console.print(table)

console.print(
    " :bookmark: 穿越时空,轻松,脑洞,纸片人,万人迷,抽奖抽卡 ",
    overflow="ellipsis",
    style=style,
)
