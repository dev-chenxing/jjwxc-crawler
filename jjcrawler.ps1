if (!$args[0]) { 
    python .\jjcrawler\cli.py
    return 
}
    
$NovelId = $args[0]

Set-Location .\jjcrawler
scrapy crawl novel -a id=$NovelId
Set-Location ..