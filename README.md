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
      <a href="https://www.github.com/labuladong" target="_blank"><img src="https://img.shields.io/badge/作者-@陈刑-689e75.svg?logo=GitHub"></a>
      <img alt="release version" src="https://img.shields.io/badge/release-v1.0.0-9ccca4">
      <img alt="last commit" src="https://img.shields.io/github/last-commit/amaliegay/jjwxc-crawler?color=7fbc87">
  </p>
</div>

<h4 align="center">
    <p>
        <b>简体中文</b> |
        <a href="https://github.com/amaliegay/jjwxc-crawler/blob/main/README_en.md">English</a>
    </p>
</h4>

### 特点功能

-   命令行界面
-   输出 DOCX 格式
-   ...................

有建议或 bug 可以提 issue.

命令行界面使用命令行 UI 库[Rich](https://github.com/Textualize/rich)编写。

界面样例：

<div align="center">
  <!--img src="post/example1.png" width="400"/>
  <img src="post/example2.png" width="400"/-->
</div>

# 安装文档

### 下载文件

点击 Code - Download ZIP，下载后解压缩得到文件夹，建议重命名为`jjwxc-crawler`

### 环境配置

-   Python 3.9.15
-   Windows

安装 Python 后，第一步，打开所在目录的命令行，输入以下命令创建并激活虚拟环境

```powershell
python -m venv venv   # 创建名为venv的Python虚拟环境
venv\Scripts\activate # Windows系统下激活虚拟环境venv
```

此时命令行前应显示有`(venv)`，表示当前已激活虚拟环境`venv`

第二部，在虚拟环境内安装 Scrapy 和其他依赖

```powershell
pip install -r requirements.txt
```

### 运行小程序

```powershell
# 进入程序所在目录
cd jjcrawler

# 运行爬虫命令，其中ID为书号
scrapy crawl novel -a id=ID

# 例如，我要下载书号为1的测试文，则运行以下命令行
scrapy crawl novel -a id=1
```

下载章节将保存至根目录下的 novels 文件夹

**[⬆ 回到顶部](#特点功能)**
