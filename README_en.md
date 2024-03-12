<a href="https://www.jjwxc.net//"><img align="right" src="assets/logo.png" alt="jjwxc-logo" title="jjwxc" width="220"></a>

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
    <img alt="last commit" src="https://img.shields.io/github/last-commit/amaliegay/jjwxc-crawler?color=7fbc87">
</p>

<h4 align="center">
    <p>
        <a href="https://github.com/amaliegay/jjwxc-crawler">简体中文</a> |
        <b>English</b>
    </p>
</h4>

Features:

-   Fluent GUI, with download progress bar and book cover display.
-   Customize download directory.
-   With Terminal User Interface.
-   Output in .docx format.
-   Supports multiple books download at the same time.
-   ...................

If you have any suggestion or have found any bug, open an issue.

The GUI was built with [PyQt-Fluent-Widgets](https://pyqt-fluent-widgets.readthedocs.io/en/latest/index.html).

A portable executable is available in [Releases](), which has both the graphical user interface and the console app.

Preview:

<div align="center">
  <!--img src="post/example1.png" width="400"/>
  <img src="post/example2.png" width="400"/-->
</div>

# Install and Usage

## Method 1: Run the .exe

A portable executable is available in [Releases](), which has both the graphical user interface and the console app.

Simply run the jjcrawler.exe and you are good to go!

## Method 2: Run the python scripts (Recommanded)

### Install Requirements

```
Python 3.8
```

```
pip install -r requirements.txt -i https://pypi.org/simple/
```

### Run the Console App

```powershell
# Launch the app
jjcrawler

# Download all non-V chapters of the novel with the id 8508851 in the directory D:/some/random/directory
jjcrawler -o D:/some/random/directory 8508851 
```


### Run the GUI

```
jjcrawler-gui
```

