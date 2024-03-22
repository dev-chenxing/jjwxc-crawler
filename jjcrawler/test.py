import time
from time import sleep
from rich import print
from rich.panel import Panel
from rich.progress import Progress, TextColumn, BarColumn, track

chapters = ["h", "e", "l", "l", "o", " ", "w", "o", "r", "l", "d"]

for i in track(range(len(chapters)), description="下载中"):
    sleep(0.2)

print("下载完毕！")

progress_bar = Progress(
    TextColumn("下载中", justify="left"),
    BarColumn(),
    "[progress.percentage]{task.percentage:>3.1f}%",
    auto_refresh=False,
)
task = progress_bar.add_task("overall", total=len(chapters))

with progress_bar:
    for chapter_no, chapter in enumerate(chapters):
        progress_bar.update(task, advance=1)
        sleep(0.2)


progress_bar.log("下载完毕！")
