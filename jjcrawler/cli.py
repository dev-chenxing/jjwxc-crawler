import os
from rich import print
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

print(
    Panel(
        "            [bold]重生之我在绿江刮刮乐",
        style="dark_cyan",
        border_style="dark_cyan",
        width=48,
    )
)

Prompt.ask("[dark_cyan]  :mag: 请输入书号")

print(
    Panel(
        "[bold]穿进百合游戏怎么办[/]\n"
        + "[white]木云杉\n"
        + "原创-百合-近代现代-爱情\n"
        + "穿进百合攻略游戏[/]\n"
        + ":bookmark: [dark cyan]穿越时空,轻松,脑洞,纸片人,万人迷,抽奖抽卡[/]",
        style="dark_cyan",
        border_style="dark_cyan",
        width=48,
    )
)

Prompt.ask("[bold dark_cyan] :floppy_disk: 一键下载 (d)[/] / 自定义下载 (c) / 返回 (b)")
