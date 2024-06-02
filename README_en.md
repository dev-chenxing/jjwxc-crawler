<div align="center"><a href="https://www.jjwxc.net//"><img src="public/logo.png" alt="jjwxc-logo" title="jjwxc" width="220"></a></div>

<h1 align="center">
   Scraping Books from the 晋江文学城 Website
</h1>
<p align="center">
  Download non-V chapters of any book on 
  <a href="https://www.jjwxc.net">https://www.jjwxc.net</a> 
</p>

<p align="center">
    <img alt="language: python" src="https://img.shields.io/badge/language-Python-118629">
		<img alt="creator: chenxing" src="https://img.shields.io/badge/creator-陈刑-689e75">
    <img alt="release version" src="https://img.shields.io/badge/release-v1.0.0-9ccca4">
    <img alt="last commit" src="https://img.shields.io/github/last-commit/dev-chenxing/jjwxc-crawler?color=7fbc87">
</p>

<h4 align="center">
    <p>
        <a href="https://github.com/dev-chenxing/jjwxc-crawler">简体中文</a> |
        <b>English</b>
    </p>
</h4>

Features:

-   CLI interface.
-   Output in .docx or .txt format.
-   Customizable output path.
-   ...................

If you have any suggestion or have found any bug, open an issue.

The CLI was built with [Rich](https://github.com/Textualize/rich).

Preview:

<div align="center">
  <img src="public/preview.gif" width="800px"/>
</div>

# Install and Usage

## Download the Source Code

Click Code - Download ZIP to download the source code. Unzip it and rename it to `jjwxc-crawler` (recommended).

### Install Requirements

-   Python 3.9.15
-   Windows

Assuming you now have Python installed, first, open a terminal in the root directory, that is, `\jjwxc-crawler`, and run the following commands to create and activate a virtual environment.

```powershell
python -m venv venv
venv\Scripts\activate # on Windows
```

If you're on Linux,

```bash
chmod +x venv/bin/activate 
source venv/bin/activate 
```

Second, install Scrapy and other dependencies within the virtual environment, so make sure your `venv` virtual environment is activated.

```powershell
pip install -r requirements.txt
```

### Run the Console App

```powershell
cd jjcrawler

# Download all non-V chapters of the novel with the specified id in the directory .\novels
scrapy crawl novel -a id=ID

# For example, like this
scrapy crawl novel -a id=1
```

Default output format is .docx

If you would like to download the chapters in .txt format, please edit `\jjcrawler\jjcrawler\spiders\config.py`

```python
# docx | txt
format = "txt"
```

**[⬆ Back to Top](#特点功能)**
