# Scraped Job Data 
Download the CSV you want, or scrape your own data.

## Thank you to:

* [Selenium](https://selenium-python.readthedocs.io/) - A tool designed for QA testing, but that actually works great for making these types of bots
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/doc) - A tool to scrape HTML/XML content (that saved be *big time* with this project)
* [Kenarapfaik](https://github.com/arapfaik/scraping-glassdoor-selenium)

## Installation
1. Install [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) (or an alternatie driver for your browser of choice):
2. Install Selenium: `pip install selenium`
3. Install BeautifulSoup: `pip install beautifulsoup4`

## Usage
1. Use keyword to control which jobs you want to get, and loc for the location.  get_jobs will get these jobs.
2. Use page_limit, which is a workaround for the page limit that only allows you to get 1000 jobs from each category if you are looking for more data.


## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/harshibar/5-python-projects/blob/master/LICENSE) file for details.
