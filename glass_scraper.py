#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 23:24:20 2020

@author: picklesueat
"""


# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 09:32:36 2020
author: Kenarapfaik
url: https://github.com/arapfaik/scraping-glassdoor-selenium
"""
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import urllib.request
from bs4 import BeautifulSoup


keyword = 'Data Analyst'
url = "https://www.glassdoor.com/blog/tag/job-search/"


#Inputs keyword and loc, and bring you to the Job Listings
def go_to_listings(driver, loc):

    
       # wait for the search bar to appear
    element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='sc.keyword']"))
        )

    try:
        # look for search bar field
        position_field = driver.find_element_by_xpath("//*[@id='sc.keyword']")
        location_field = driver.find_element_by_xpath("//*[@id='sc.location']")
        

        # fill in with pre-defined data
        position_field.clear()
        position_field.send_keys(keyword)
        
        location_field.clear()
        location_field.send_keys(loc)

        # wait for a little so location gets set
        time.sleep(3)
        driver.find_element_by_xpath(" //*[@id='HeroSearchButton']").click()

        # close a random popup if it shows up
        try:
            driver.find_element_by_xpath("//*[@id='JAModal']/div/div[2]/span").click()
        except NoSuchElementException:
            pass
        
        time.sleep(3)
        
            
        try:
            driver.find_element_by_xpath("//*[@id='JAModal']/div/div[2]/span").click()
        except NoSuchElementException:
            pass
  
    except NoSuchElementException:
        pass

#Initializes driver, and navigates to URL
def initialize_driver(path):
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    

    ua = UserAgent()
    userAgent = ua.random
    options.add_argument(f'user-agent={userAgent}')
    
    #makes the driver more 'undetectale'
    options.add_argument("--disable-blink-features"), options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.maximize_window()

    
    return driver

def Xout_pop_ups(driver):
        #Test for the "Sign Up" prompt and get rid of it.
    time.sleep(2)
    try:
        driver.find_element_by_class_name("selected").click()
    except Exception:
        pass

    time.sleep(.1)

    #X out pop-up
    try:
        driver.find_element_by_css_selector('[alt="Close"]').click() #clicking to the X.
    except Exception:
        pass
    
    
def click_listing(driver, job_button):
    illstatus = 'Fine'
    try:
        job_button.click()#You might
        
    except Exception:
        illstatus = 'Ill'
        time.sleep(1)
        try:
            job_button.click()
            illstatus = 'Illness Corrected'
        except Exception:
            illstatus = 'Failed'
        
    return illstatus
        
    
def collect_listing_info(driver, slp_time, verbose):
    time.sleep(slp_time)
    collected_successfully = False
    no_load_time = 0
    while not collected_successfully:
        #If page has timed out from not-loading, restart the process by clicking first listing

        if(no_load_time >= 10):
            driver.find_element_by_xpath("//*[@id='MainCol']/div[1]/ul/li[1]").click()

            
        try:
            driver.find_element_by_xpath("//*[@id='HeroHeaderModule']/div[3]/div[2]/div/div[1]/div[2]/button")
            
        except NoSuchElementException:
            no_load_time +=1
        try:
            company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
            location = driver.find_element_by_xpath('.//div[@class="location"]').text
            job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
            job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
            collected_successfully = True
        except:
            time.sleep(5)

    try:
        salary_estimate = driver.find_element_by_xpath('.//span[@class="gray salary"]').text
    except NoSuchElementException:
        salary_estimate = -1 #You need to set a "not found value. It's important."
    
    try:
        rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
    except NoSuchElementException:
        rating = -1 #You need to set a "not found value. It's important."

    #Printing for debugging
    if verbose:
        print("Job Title: {}".format(job_title))
        print("Salary Estimate: {}".format(salary_estimate))
        print("Job Description: {}".format(job_description[:500]))
        print("Rating: {}".format(rating))
        print("Company Name: {}".format(company_name))
        print("Location: {}".format(location))

    #Going to the Company tab...
    #clicking on this:
    #<div class="tab" data-tab-type="overview"><span>Company</span></div>
    try:
        driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()

        try:
            #<div class="infoEntity">
            #    <label>Headquarters</label>
            #    <span class="value">San Francisco, CA</span>
            #</div>
            headquarters = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
        except NoSuchElementException:
            headquarters = -1

        try:
            size = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
        except NoSuchElementException:
            size = -1

        try:
            founded = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
        except NoSuchElementException:
            founded = -1

        try:
            type_of_ownership = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
        except NoSuchElementException:
            type_of_ownership = -1

        try:
            industry = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
        except NoSuchElementException:
            industry = -1

        try:
            sector = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
        except NoSuchElementException:
            sector = -1

        try:
            revenue = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
        except NoSuchElementException:
            revenue = -1

        try:
            competitors = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
        except NoSuchElementException:
            competitors = -1

        
        try:
            easy_apply = (driver.find_element_by_xpath('//*[@id="HeroHeaderModule"]/div[3]/div[2]/div/div[1]/div[1]/button/span').text  == 'Easy Apply')
        except NoSuchElementException:
            easy_apply = -1

    except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
        headquarters = -1
        size = -1
        founded = -1
        type_of_ownership = -1
        industry = -1
        sector = -1
        revenue = -1
        competitors = -1
        easy_apply = -1

        
    if verbose:
        print("Headquarters: {}".format(headquarters))
        print("Size: {}".format(size))
        print("Founded: {}".format(founded))
        print("Type of Ownership: {}".format(type_of_ownership))
        print("Industry: {}".format(industry))
        print("Sector: {}".format(sector))
        print("Revenue: {}".format(revenue))
        print("Competitors: {}".format(competitors))
        print("Easy Apply: {}".format(easy_apply))
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    jobinfo = ({"Job Title" : job_title,
    "Salary Estimate" : salary_estimate,
    "Job Description" : job_description,
    "Rating" : rating,
    "Company Name" : company_name,
    "Location" : location,
    "Headquarters" : headquarters,
    "Size" : size,
    "Founded" : founded,
    "Type of ownership" : type_of_ownership,
    "Industry" : industry,
    "Sector" : sector,
    "Revenue" : revenue,
    "Competitors" : competitors,
    "Easy Apply": easy_apply})
    
    return jobinfo

def make_sure_jobs(driver):
    try:
        if(driver.find_element_by_xpath("//*[@id='MainCol']/div[1]/div[2]/div/div[1]/p/span[2]").text.split(' ' )[1] == 'search'):
            driver.refresh()
            time.sleep(5)
            if(driver.find_element_by_xpath("//*[@id='MainCol']/div[1]/div[2]/div/div[1]/p/span[2]").text.split(' ' )[1] == 'search'):
                return 'X'


    except Exception:
        pass
        
    try:
        print(driver.find_element_by_xpath("//*[@id='MainCol']/div[1]/div[2]/div/div/h4").text.split(' ' )[1])
        if((driver.find_element_by_xpath("//*[@id='MainCol']/div[1]/div[2]/div/div/h4").text.split(' ' )[1] == 'search')):
            driver.refresh()
            time.sleep(5)
            if((driver.find_element_by_xpath("//*[@id='MainCol']/div[1]/div[2]/div/div/h4").text.split(' ' )[1] == 'search')):
                return 'X'


    except Exception:
        pass
    
def get_jobs(keyword, num_jobs, verbose, path, slp_time, loc = ' ', driver = ' '):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    count = 0 

    if(loc == ' '):
        driver = initialize_driver(path)
    
    driver.get(url)
    go_to_listings(driver,loc)
           
    

    
    
    
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.

        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='HeroSearchButton']"))
        )


        #Test for the "Sign Up" prompt and get rid of it.
        Xout_pop_ups(driver)

        x = make_sure_jobs(driver)
        if(x == 'X'):
            break

        #Going through each job in this page
        time.sleep(1.5)
        job_buttons = driver.find_elements_by_css_selector("li.jl.react-job-listing.gdGrid")  #jl for Job Listing. These are the buttons we're going to click.
        if(len(job_buttons) <=25):
            print("JOBS PER PAGE: " + str(len(job_buttons)))
        for job_button in job_buttons: 
            if len(jobs) >= num_jobs:
                print("Job Target Reached:" + str(len(jobs)) + '/' + str(num_jobs))
                break

            status = click_listing(driver, job_button)

            #Weird error pops up here, so I'm on the lookout,
            if(status == 'Failed'):
                print(status)
                break

            #append listing data, to total list for that location 
            jobs.append(collect_listing_info(driver, slp_time, verbose = verbose))

        page_num = driver.find_element_by_xpath("//*[@id='ResultsFooter']/div[1]").text
        page_num = page_num.split(' ')
        if(page_num[1] == page_num[3]):
            break
        
        #Clicking on the "next page" button
        try:
            if(count<=33):
                driver.find_element_by_xpath('.//li[@class="next"]//a').click()
                count +=1
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    
    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.


def page_limit(keyword, num_jobs, verbose, path, slp_time, start_at = 0):
    driver = initialize_driver(path)
    #General Location
    if(start_at == 0):
        df = get_jobs(keyword, 1, verbose, path, slp_time)
        df = df[0:0]
        df.to_csv('Jobs_apply/glassdoor_job_data/' + keyword.replace(' ', '') + '.csv', index = False)
    
    cities = top_cities()
    
    for x in range(start_at,len(cities.index) - 217):
        print("City Index: " + str(x))
        try:    
            df = get_jobs(keyword, num_jobs, verbose, path, slp_time, loc = (cities.iloc[x,0] + ', ' + cities.iloc[x,1]), driver = driver)
        except Exception:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            df = get_jobs(keyword, num_jobs, verbose, path, slp_time, loc = (cities.iloc[x,0] + ', ' + cities.iloc[x,1]), driver = driver)
        df.to_csv('Jobs_apply/glassdoor_job_data/' + keyword.replace(' ', '') + '.csv', index = False, mode='a', header=False)



def top_cities():
    #scrapes the list of most populated cities from wikipedia
    url = "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    table = soup.find('table',{'class':'wikitable sortable'})
    rows = (table.find_all('tr'))
    
    city = []
    state = []
    df = pd.DataFrame()
    rows.pop(0)
    for row in rows: 
        data = row.find_all('a')
        city.append(data[0].text)
        state.append(row.find_all('td')[2].text.replace('\n',''))
        
    city = pd.Series(city)
    state = pd.Series(state)
    df['City'] = city
    df['State'] = state
    
    
#to test program    
page_limit(keyword,500, False, chromedriver path, 2.5, start_at = 0)
