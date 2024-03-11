<!--div align="center">
  <img src="assets/logo.png" width="256"/>
</!--div-->

<a href="https://www.jjwxc.net//"><img align="right" src="assets/logo.png" alt="jjwxc-logo" title="jjwxc" width="220"></a>

<div>
  <h1 align="center">
  《重生之我在绿江爪爪巴》
</h1>
<p align="center">
  一键下载
  <a href="https://www.jjwxc.net">晋江文学城 (https://www.jjwxc.net)</a> 
  网站小说非 V 章节
</p>
<p align="center">
    <img alt="language: python" src="https://img.shields.io/badge/language-Python-118629">
    <img alt="creator: chenxing" src="https://img.shields.io/badge/creator-陈刑-689e75">
    <img alt="release version" src="https://img.shields.io/badge/release-v1.0.0-9ccca4">
    <img alt="last commit" src="https://img.shields.io/github/last-commit/amaliegay/jjwxc-scrape?color=7fbc87">
</p>
</div>

<h4 align="center">
    <p>
        <b>简体中文</b> |
        <a href="https://github.com/amaliegay/jjwxc-scrape/blob/main/README_en.md">English</a>
    </p>
</h4>

### 特点功能

-   提供 Fluent 用户界面，下载进度与书籍封面显示。
-   下载目录自定义。
-   同时支持命令行版本。
-   输出可选 DOCX、TXT 格式。
-   支持书籍批量下载。
-   ...................

有建议或 bug 可以提 issue.

图形界面使用[PyQt-Fluent-Widgets](https://pyqt-fluent-widgets.readthedocs.io/en/latest/index.html)界面编写。

[Releases]()页面发布了已经打包好的 exe 可执行程序，包括图形化版本和命令行版本。

界面样例：

<div align="center">
  <!--img src="post/example1.png" width="400"/>
  <img src="post/example2.png" width="400"/-->
</div>

# 快速上手

## 方法一、运行 exe

[Release]()页面发布了已经打包好的 exe 可执行程序，包括图形化版本和命令行版本。

用户只需要双击 exe 就可以使用啦！

## 方法二、运行 python 脚本（推荐）

### 使用前安装需要的包

-   Python 3.8+

安装 Python 后在 cmd 输入以下命令行安装所需的包

```
pip install -r requirements.txt -i https://pypi.org/simple/
```

### 使用命令行模式运行

```powershell
# 启动程序
jjscrape

# 下载书号为8508851的小说的所有非V章节到D:/some/random/directory文件夹
jjscrape -o D:/some/random/directory 8508851
```

### 使用图形界面运行

```
jjscrape_gui
```

**[⬆ 回到顶部](#特点功能)**
