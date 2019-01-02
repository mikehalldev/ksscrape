# ksscrape
ksscrape is an easy way to scrape project information from [kickstarter's discovery page](https://www.kickstarter.com/discover) using Python with Selenium.

## Installation
ksscrape.search.DiscoverySearcher requires a Selenium webdriver object. Download [ChromeDriver](http://chromedriver.chromium.org/downloads) (or any webdriver) and add it to your PATH environment variable for easy access.

Run the following commands to install ksscrape.
```
git clone https://github.com/televisedprogram/ksscrape.git
pip install ./ksscrape/ --upgrade
```

## Usage
```
from selenium import webdriver
from ksscrape.search import DiscoverySearcher

driver = webdriver.Chrome()

searcher = DiscoverySearcher(driver)
searcher.get_search_page(category='Games', sort_by='Newest', sub_category='Video Games')
searcher.scroll_until_count(100)

data = searcher.get_projects_dictionaries()
```