# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 07:58:47 2022

@author: SAKURA-x
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller

from bs4 import BeautifulSoup
import time

#import pyperclip
import csv

import requests
import re
import os
import random

import datetime
import threading

import warnings
warnings.filterwarnings("ignore")
chromedriver_autoinstaller.install()


driver = ''
DATETYPE = '%Y-%m-%d'
# DATETYPE2 = '%Y.%m.%d'

def DateToString(value):
    if value == 'now':
        value = datetime.datetime.now()
        
    # day = value.day    
    # month = value.month
    
    # if len(str(day)) == 1:
    #     day = '0' + str(day)
            
    # if len(str(month)) == 1:
    #     month = '0' + str(month)
    
    # String = str(year)+str(month)+str(day)    
    String = value.strftime(DATETYPE)
    return String  

def StringToDate(value):
    return datetime.datetime.strptime(value, DATETYPE)

# def StringToDate2(value):
#     return datetime.datetime.strptime(value, DATETYPE2)

def StringToDateV2(value, tDATETYPE = DATETYPE):
    return datetime.datetime.strptime(value, tDATETYPE)

def IncreaseDate(nowDateString, value, val):
    
    date = StringToDate(nowDateString)
    if value == 'day':
        date = date + datetime.timedelta(days=val)
    elif value == 'second':
        date = date + datetime.timedelta(seconds=val)

    String = date.strftime(DATETYPE)
    
    return String


# STARTDATE = '2017-01-01'
# ENDDATE = DateToString('now')

import itertools

def xpath_soup(element):
    """
    Generate xpath of soup element
    :param element: bs4 text or node
    :return: xpath as string
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)



def scrollDown(driver):
    for i in range(6):
        ActionChains(driver).send_keys(Keys.DOWN).perform()


def scrollDownTime(driver, sec):
    for i in range(sec):
        for i in range(6):
            ActionChains(driver).send_keys(Keys.DOWN).perform()
        time.sleep(1)

def overTimer():
    global driver
    print('최대 탐색 시간 초과')
#    iterate = False
    driver.close()
#    raise ValueError('over search time')

def clickXpathByClass(classId, string):
    global driver
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    numList = soup.find_all(class_= classId)

    nextNum = numList[0].findNext('a')
    while(True):
        if string == str(nextNum.getText()):
            break
        nextNum = nextNum.findNext('a')
    
    xpath = xpath_soup(nextNum)
    selenium_element = driver.find_element_by_xpath(xpath)
#    ActionChains(driver).move_to_element(selenium_element).perform()
    selenium_element.click()



def readCsv(path):
    f = open(path, 'r', encoding='utf-8')
    cin = csv.reader(f, delimiter=',')
    temp = [row for row in cin]
    f.close()
    return temp

allCount = 0
ipAddr = ''
timer = ''


  # if text != getText:
        # text = getText
        # #listout.append(text)
        # f = open('url_tracer_output.csv', 'a', newline='', encoding='utf-8')
        # wr = csv.writer(f)
        # wr.writerow([text])
        # outTime = time.time() - s
        # wr.writerow([outTime])
        # s = time.time()        
        # print(text)
        # f.close()
            
            
words = readCsv('../keyword.txt')
print('검색어 :', words)

driver = webdriver.Chrome()

for word in words:
    word = word[0]

    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='+word
    driver.get(url)

    for _ in range(3):
        ActionChains(driver).send_keys(Keys.END).perform()
        time.sleep(0.5)


     
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    numList = soup.find_all(class_= 'api_more_wrap')


    clickList = readCsv('../search.txt')
    #clickList = ['후기 더보기','참여 콘텐츠 더보기','팁 모음 더보기']


    _urlList = []

    for num in numList:
        num = num.findNext('a')
        for click in clickList:
            if str(num.getText()).find(click[0]) != -1:
                
                _urlList.append(num['href'])
                #xpath = xpath_soup(num)
                #selenium_element = driver.find_element_by_xpath(xpath)
                #    ActionChains(driver).move_to_element(selenium_element).perform()
                #   selenium_element.click()
                 
                time.sleep(1)
                
    for _url in _urlList:
        driver.get(_url)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        numList = soup.find_all(class_= 'group_inner')
        
        for num in numList:
            #print(num.findNext('a').getText(), num.findNext('a')['href'], str(num.findNext('a')['href']).replace('https://','').split('/')[1])
            f = open('../result_'+DateToString('now')+'.txt', 'a', newline='', encoding='utf-8')
            wr = csv.writer(f)
            wr.writerow([word, num.findNext('a').getText(), num.findNext('a')['href'], str(num.findNext('a')['href']).replace('https://','').split('/')[1]])
            f.close()
        
driver.close()   
        
        
        # outTime = time.time() - s
        # wr.writerow([outTime])
        # s = time.time()        
        # print(text)
        
        
        
        
        # if num.findNext('a')['href'] == '#':
            # num = num.findNext('a')
            # print(num.findNext('a')['href'])
        # else:
            # print(num.findNext('a')['href'])
    






# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')
# numList = soup.find_all(class_= 'api_more_wrap')
            
# while(True):
    # if string == str(nextNum.getText()):
        # break
    # nextNum = nextNum.findNext('a')

# xpath = xpath_soup(nextNum)
# selenium_element = driver.find_element_by_xpath(xpath)
# #    ActionChains(driver).move_to_element(selenium_element).perform()
# selenium_element.click()

        # #print(driver.title)
        
        # timer = threading.Timer(1201, overTimer)
        # timer.start()

        # time.sleep(2)
        # driver.get("https://naver.com")
        
        
        

            
            
            
            
            
            
        

