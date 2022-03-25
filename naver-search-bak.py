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


def getMobileBlogNic():
    global driver
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    numList = soup.find_all('div')
    
    for num in numList:
        try:
            if str(num['class']).find('nickname') != -1:
                return num.getText()
        except:
            pass
    
    return -1


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

try:
    size = readCsv('./size.txt')
except:
    size = readCsv('../size.txt')

size = int(size[0][0])
print('검색 사이즈 :', size)

try:
    message = readCsv('./message.txt')
except:
    message = readCsv('../message.txt')

text = ''
for _m in message:
    text += (_m[0])


overTime = len(words) * 2 * size


#if timer != '': 
#    timer.cancel()
#
#timer = threading.Timer(overTime, overTimer)
#timer.start()


options = webdriver.ChromeOptions() 
#options.add_argument("--auto-open-devtools-for-tabs")

mobile_emulation = { "deviceName": "Nexus 5" }

options.add_experimental_option("mobileEmulation", mobile_emulation)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
#driver = webdriver.Chrome(options=options, executable_path=r'../chromedriver_win3298/chromedriver')
driver = webdriver.Chrome(options=options)

#driver = webdriver.Chrome()

for word in words:
    word = word[0]
    print(word)
    
    
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='+word
    driver.get(url)

    for _ in range(3):
        ActionChains(driver).send_keys(Keys.END).perform()
        time.sleep(0.5)


     
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #numList = soup.find_all(class_= 'api_more_wrap')
    numList = soup.find_all('a')


    clickList = readCsv('../search.txt')
    #clickList = ['후기 더보기','참여 콘텐츠 더보기','팁 모음 더보기']


    _urlList = []

    for num in numList:
#        num = num.findNext('a')
        for click in clickList:
            if str(num.getText()).find(click[0]) != -1:
                if str(num['href']).find('https://in.naver.com/') == -1:
                    _urlList.append(num['href'])
                #xpath = xpath_soup(num)
                #selenium_element = driver.find_element_by_xpath(xpath)
                #    ActionChains(driver).move_to_element(selenium_element).perform()
                #   selenium_element.click()
                 
                    time.sleep(0.5)
                
                
#    for _url in _urlList:
#    
#        if str(_url)[0] == '?':
#            _url = 'https://search.naver.com/search.naver'+_url
#        
#        driver.get(_url)
#        
#        html = driver.page_source
#        soup = BeautifulSoup(html, 'html.parser')
#        numList = soup.find_all(class_= 'group_inner')
#        
#        for num in numList:
#            #print(num.findNext('a').getText(), num.findNext('a')['href'], str(num.findNext('a')['href']).replace('https://','').split('/')[1])
#            f = open('../result_'+DateToString('now')+'.txt', 'a', newline='', encoding='utf-8')
#            wr = csv.writer(f)
#            wr.writerow([word, num.findNext('a').getText(), num.findNext('a')['href'], str(num.findNext('a')['href']).replace('https://','').split('/')[1]])
#            f.close()

    NaverIDtoBlog_all = {}
    NaverIDtoIn_all = {}
    
    for _url in _urlList:
    
        if str(_url)[0] == '?':
#            _url = 'https://search.naver.com/search.naver'+_url
        #모바일
            _url = 'https://m.search.naver.com/search.naver'+_url
        driver.get(_url)
        
        for _ in range(5):
            ActionChains(driver).send_keys(Keys.END).perform()
            time.sleep(1)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        numList = soup.find_all('a')
        
        getNaverIDtoIn = []
        getNaverIDtoBlog = []
        
        except_words = ['naver_search', 'MyBlog.naver', 'nidlogin.login', 'influencer_search', 'nidlogin.login', 'challenge']
        
        for num in numList:
            try:
                if str(num['href']).find('https://in.naver.com/') != -1:
#                    for _word in except_words:
#                        if str(num['href']).find(_word) == -1:
                    getNaverIDtoIn.append(num['href'])
                
#                if str(num['href']).find('https://blog.naver.com/') != -1:
                if str(num['href']).find('blog.naver.com/') != -1:
                    getNaverIDtoBlog.append(num['href'])
                    
                    
#                if str(num['href']).find('https://blog.naver.com/') != -1:
#                    getNaverIDtoBlog.append(num['href'])
            except:
                pass
        
        
        NaverIDtoBlog = {}
        for _idLink in getNaverIDtoBlog:
            isExceptWord = False
            for _word in except_words:
                if str(_idLink).find(_word) != -1:
                    isExceptWord = True
                    break
            if isExceptWord:
                continue
        
            _id = str(_idLink).replace('https://','').split('/')[1]
            
            NaverIDtoBlog[_id] = 1
            
            if len(NaverIDtoBlog) >= size:
                break
        

        NaverIDtoIn = {}
        for _idLink in getNaverIDtoIn:
            isExceptWord = False
            for _word in except_words:
                if str(_idLink).find(_word) != -1:
                    isExceptWord = True
                    break
            if isExceptWord:
                continue
            
#            if str(_idLink).find('?query') != -1:
#                continue
            
            _id = str(_idLink).replace('https://','').split('/')[1].split('?')[0]
            
            NaverIDtoIn[_id] = 1
            
            if len(NaverIDtoIn) >= size:
                break
        
        
        ##여기에 중복제거 로직 추가
        for __ID in NaverIDtoIn.keys():
            NaverIDtoIn_all[__ID] = 1
            
        for __ID in NaverIDtoBlog.keys():
            NaverIDtoBlog_all[__ID] = 1

        
    #블로그를 탐색하며 실 ID 체크 및 NICNAME 체크  
    datalist = []
    for k in NaverIDtoBlog_all.keys():
        if k == '':
            continue
        
        dic = {}
        dic['keyword'] = word
        try:
            _type = '블로거'
            __url = 'https://blog.naver.com/'+k
            driver.get(__url)
            dic['id'] = k
            dic['type'] = _type
            
#                driver.switch_to.frame('mainFrame')
#                _name = driver.find_element_by_xpath('//*[@id="nickNameArea"]').text
#                dic['name'] = _name
            
            _name = getMobileBlogNic()
            if _name == -1:
                continue
            
            dic['name'] = str(_name).replace('마켓블로그','').replace('공식 블로그','')
            
            datalist.append(dic)
            
            f = open('../result_'+DateToString('now')+'.txt', 'a', newline='', encoding='utf-8')
            wr = csv.writer(f)
            wr.writerow([word, k, _type, _name])
            f.close()
            
            sendText = text.replace('{{ID}}', k).replace('{{Type}}', _type).replace('{{Name}}', _name)
            
            f = open('../result_form_'+DateToString('now')+'.txt', 'a', newline='', encoding='utf-8')
            wr = csv.writer(f)
            wr.writerow([sendText])
            f.close()
            
            time.sleep(0.7)
        except:
            pass
        
    
    for k in NaverIDtoIn_all.keys():
        
        if k in list(NaverIDtoBlog_all.keys()):
            continue
            
        if k == '':
            continue
        
        dic = {}
        dic['keyword'] = word
        try:
            
            _type = '인플루언서'
            __url = 'https://blog.naver.com/'+k
            driver.get(__url)
            dic['id'] = k
            dic['type'] = _type
            
#                driver.switch_to.frame('mainFrame')
#                _name = driver.find_element_by_xpath('//*[@id="nickNameArea"]').text
#                dic['name'] = _name
            
            _name = getMobileBlogNic()
            if _name == -1:
                continue
            
            dic['name'] = str(_name).replace('마켓블로그','').replace('공식 블로그','')
            
            datalist.append(dic)
            
            f = open('../result_'+DateToString('now')+'.txt', 'a', newline='', encoding='utf-8')
            wr = csv.writer(f)
            wr.writerow([word, k, _type, _name])
            f.close()
            
            sendText = text.replace('{{ID}}', k).replace('{{Type}}', _type).replace('{{Name}}', _name)
            
            f = open('../result_form_'+DateToString('now')+'.txt', 'a', newline='', encoding='utf-8')
            wr = csv.writer(f)
            wr.writerow([sendText])
            f.close()
            
            time.sleep(0.7)
            
        except:
            pass
        



#<a target="_blank" href="https://in.naver.com/iamchocolat?query=%EB%AF%B8%EC%8A%A4%ED%8A%B8+%EC%B0%B8%EC%97%AC+%EC%BD%98%ED%85%90%EC%B8%A0" class="name" onclick="goOtherCR(this, 'a=itb_bas*f.profile&amp;r=19&amp;i=SPC-0000000000006816.a0209rl4_nblog_post_222653959305&amp;g=%7B%22bid%22%3A%22SPC-0000000000006816%22%2C%22docRank%22%3A1%7D&amp;u='+urlencode(this.href));">쇼콜라</a>
#        <a target="_blank" href="https://in.naver.com/cosreader?query=%EB%B7%B0%EB%9F%AC" class="name elss" onclick="return goOtherCR(this,'a=ink_kib*a.nickname&amp;r=1&amp;i=a0209rl4_nblog_post_222652147919&amp;u='+urlencode(this.href))"><span class="txt">화장품읽어주는남자</span></a>
#        
        
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
        
        
        

            
            
            
            
            
            
        

