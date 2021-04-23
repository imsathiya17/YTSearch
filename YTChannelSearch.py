import datetime
import sys
from concurrent.futures import ThreadPoolExecutor, wait
from time import sleep, time
from configparser import ConfigParser
import os
import ssl
import pandas as pd
from pandas import DataFrame
from openpyxl.workbook import Workbook

import csv
from pathlib import Path
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup

import os
import json
from youtubesearchpython import *
from youtubesearchpython import ChannelsSearch

def FetchData(ChannelURL,browser):
    
    print(f"Fetching channel Information ######################################### {ChannelURL}...") 
    
    if connect_to_base(browser, ChannelURL):
        
        html = browser.page_source
    
          
def run_process(stashBase,browser):
    
    OpenRequests = []
         
    print(f"Fetching open Requests ######################################### {PullReqOpen}...") 
          
    if connect_to_base(browser, PullReqOpen):
        
        html = browser.page_source
        
        OpenRequests=getOpenRequests(html,stashBase,users)
       
        
        for request in OpenRequests:
            
            print(request[0]+'-'+request[1])
            
            if connect_to_approve(browser,str(request[1])):
                  
                try:
                    
                    selfApproveButton=browser.find_element_by_xpath("//button[@class='manage-self-button add-self']")
                    selfApproveButton.click()
                                        
                    #approveButton=browser.find_element_by_xpath("//button[@data-testid='toggle-approve-pull-request']")
                    #approveButton.click()
                    
                    
                except:
                    
                    print('add self approve cannot be performed.')
                    
                try:
                    
                    sleep(2)
                    
                    approveButton=browser.find_element_by_xpath("//button[@aria-label='Approve: This pull request is ready to merge']")
                    approveButton.click()
                    
                except:
                    
                    print("Cannot perform auto approve on this request since its already approved.")    
                
                
                
            else:
                
                print(f"Cannot fetch approve request url ######################################### {request[1]}...")
            
        #browser.quit()
        
    else:
        print(f"No open requests found at the moment for repository ######################################### {PullReqOpen}...")
        #browser.quit()
        

def get_driver():
        # Start a new browser and return the WebDriver
        
        fireFoxOptions = webdriver.ChromeOptions()
        fireFoxOptions = Options()

        fireFoxOptions.headless = False
        browser = webdriver.Chrome(options=fireFoxOptions)
        
        return browser

def connect_to_base(browser, PullReqOpen):
    
    base_url = PullReqOpen
    
    print("Jenkins Pull Request url:- "+base_url)

    try:
            browser.get(PullReqOpen.strip())
            # wait for table element with id = 'hnmain' to load
            # before returning True
            wait = WebDriverWait(browser, 5)
            wait.until(visibility_of_element_located((By.XPATH, "//*[@class='style-scope ytd-item-section-renderer']")))
            return True
            
    except:
            print(f"WARNING: required elements not loaded to get open requests from {base_url}.")
            return False


def connect_to_approve(browser, request):
    
    base_url = request
    
    print("Jenkins Pull Request url:- "+base_url)

    try:
            browser.get(request.strip())
            # wait for table element with id = 'hnmain' to load
            # before returning True
            wait = WebDriverWait(browser, 10)
            wait.until(visibility_of_element_located((By.XPATH, "//*[@class='aui-page-panel-inner']")))
            return True
            
    except:
            print(f"WARNING: required elements not loaded to approve from {base_url}.")
            return False


def getOpenRequests(html,stashBase,users):
    
    soup = BeautifulSoup(html,features="lxml")
    
    output_list=[]
    #table = soup.find('table', {'class': 'aui paged-table pull-requests-table'})
    tab = soup.find("table",{"class":"aui paged-table pull-requests-table"})
    rows = tab.findAll('tr')
    for tr in rows:
        cols = tr.findAll('td')
        if len(cols) != 0:
            CorpID = cols[1].get('data-username')
            PullRequestLink = stashBase+cols[1].find('a').get('href')
            
            output=[CorpID,PullRequestLink]
            
            if CorpID in users:
                output_list.append(output)
                
                print(CorpID+'-'+PullRequestLink) 
                     
          
    return output_list


def get_load_time(article_url):
    try:
        # set headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
        }
        # make get request to article_url
        response = requests.get(
            article_url, headers=headers, stream=True, timeout=3.000
        )
        # get page load time
        load_time = response.elapsed.total_seconds()
        
    except Exception as e:
        print(e)
        load_time = "Loading Error"
    return load_time

def getCommitfilesList(reqURL,browser):
    
    try:
            browser.get(reqURL.strip())
            wait = WebDriverWait(browser, 10)
            wait.until(visibility_of_element_located((By.XPATH, "//*[@class='changes-tree']")))
          
    except:
            print(f"WARNING: required elements not loaded to get open requests from {reqURL}.")
            return False
  
    html=browser.page_source
            
    soup = BeautifulSoup(html,features="lxml")
    
    changeTree = soup.find("div",{"class":"changes-tree"})
    rows = changeTree.findAll('a')
    for tr in rows:
        print("File:- "+str(tr.get('href')))     
        print("fileName:- "+str(tr.find('span',{"class":"file-label"})))
        
        
if __name__ == "__main__":

    
    ssl._create_default_https_context = ssl._create_unverified_context
    

    start_time = time()
    
    stashBase="https://www.youtube.com/results?search_query=crypto&sp=EgIQAg%253D%253D"
        
    channelsSearch = ChannelsSearch('crypto', limit = 1, region = 'US')
    
    
    #ChannelsOutput=channelsSearch.result()
    
    json_object = json.dumps(channelsSearch.result(), indent = 4)  
    
    
    #print(channelsSearch.result(mode = ResultMode.json))
    
    ChannelsOutput = channelsSearch.result(mode = ResultMode.json)
    
    json=json.loads(ChannelsOutput)
    
    browser = get_driver()
    
    for Channel in json['result']:
       print(Channel['id'])
       print(Channel['title'])
       print(Channel['link'])
       
       ChannelAboutURL=Channel['link']+'/about'
       
       if str(Channel['descriptionSnippet']) != 'None':
           print(Channel['descriptionSnippet'][0])
       
       FetchData(ChannelAboutURL,browser)
            
    #run_process(stashBase,browser)
            
    #getCommitfilesList(commitURL,browser)
    
    #browser.quit()
    
    end_time = time()
    elapsed_time = end_time - start_time
        
    print(f"Elapsed run time: {elapsed_time} seconds")
