# This was a project to understand the Data Science/Engineer/Analyst job market in June 2020.
## See my [visualization of this data](https://www.kaggle.com/code/josephgutstadt/skills-for-a-data-scientist-analyst), including some basic data mining (association analysis)


# Scraped Job Data 
Download the CSV you want, or scrape your own data.

## See my analysis of this dataset [here](https://www.kaggle.com/code/josephgutstadt/skills-for-a-data-scientist-analyst/notebook)
![image](https://user-images.githubusercontent.com/9833065/188324500-604ad708-8896-4631-8d19-529d8f94b768.png)


![image](https://user-images.githubusercontent.com/9833065/188324465-97f2925a-e484-418d-a54c-ac130865743c.png)



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
