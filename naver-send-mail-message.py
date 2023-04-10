# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 07:58:47 2022

@author: SAKURA-x
"""

# from anticaptchaofficial.imagecaptcha import *

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# import chromedriver_autoinstaller

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


import urllib.request



import warnings
warnings.filterwarnings("ignore")
# chromedriver_autoinstaller.install(True)


driver = ''
DATETYPE = '%Y-%m-%d'
# DATETYPE2 = '%Y.%m.%d'

# esUrl = 'http://3.37.243.132:9200/'
esUrl = 'http://3.37.243.132:8806/dksdbgus/'

import json

esType ='data'
indexDate = ''
indexDateD = ''
bulkSize = 1000




import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()



def getdetails_qurey(esIndex, qurey, esUrl = esUrl):
    with requests.Session() as session:
        url = esUrl + esIndex + '/_search'
        body = qurey
        
        headers = {'content-type': "application/json"}
        response = session.request("POST", url, data=str(json.dumps(body)), headers=headers, verify=False, proxies={})
#        print(response.text)
        try:
            jsonString  = json.loads(response.text, encoding="utf-8")
            arr = jsonString["hits"]["hits"]
            # print(arr)
        except Exception as b:
            # print('error getIds',b)
            return {}
    return arr



def insertBulk(datalist, esIndex, esUrl = esUrl):

    make = ''
    with requests.Session() as session:
        for i in range(len(datalist)):
            
            _id = str(datalist[i][0])
            make += "{ \"index\" : { \"_index\" : \""+esIndex+"\", \"_type\" : \""+esType+"\", \"_id\" : \""+_id+"\" } }\r\n"+str(json.dumps(datalist[i][1]))+"\r\n"
            if (i != 0 and i%bulkSize == 0 ) or i == len(datalist)-1:
                print('input',i+1,'개')
                
                url = esUrl +'_bulk'
                headers = {'content-type': "application/x-ndjson"}
                response = session.request("POST", url, data=make.encode(encoding='utf-8'), headers=headers, verify=False, proxies={})
                # print(response,'200이면 성공')
                
                if str(response).find('200') == -1:
                    print('error', response.text)
                #print(response.text)
                make = ''


def updateBulk(esIndex, datalist):

    make = ''
    with requests.Session() as session:
        for i in range(len(datalist)):
            
            _id = str(datalist[i][0])
            
#            dic = {}
#            dic['doc'] = {key:value}            
            
            make += "{ \"update\" : { \"_index\" : \""+esIndex+"\", \"_type\" : \""+esType+"\", \"_id\" : \""+_id+"\" } }\r\n"+str(json.dumps(datalist[i][1]))+"\r\n"
            if (i != 0 and i%bulkSize == 0 ) or i == len(datalist)-1:
                print('input',i+1,'개')
                
                url = esUrl +'_bulk'
                headers = {'content-type': "application/x-ndjson"}
                response = session.request("POST", url, data=make.encode(encoding='utf-8'), headers=headers, verify=False, proxies={})
                print(response,'200이면 성공')
                
                if str(response).find('200') == -1:
                    print('error', response.text)
                #print(response.text)
                make = '' 



def DateToString2(value):
    
    import datetime
    
    if value == 'now':
        value = datetime.datetime.now()
  
    # String = str(year)+str(month)+str(day)    
    String = value.strftime('%Y-%m-%dT%H:%M:%S')
    String2 = value.strftime('%Y%m%d%H%M%S')
    return String, String2 


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


def makeLog(sendId, message, desId, state):
    _datalist = []
    TimeString, TimeValue = DateToString2('now')
    ed_id = TimeString
    
    dic = {}
    dic['id'] = ed_id
    dic['value'] = sendId #쪽지 보내는 아이디
    dic['state'] = message
    dic['date'] = TimeString
    dic['date2'] = TimeValue
    dic['keyword'] = desId  #쪽지 받는 아이디
    dic['type'] = state
    # 'ING'
    
    _datalist.append([ed_id, dic])
    
    insertBulk(_datalist, 'cubist_naver_log', esUrl)

def updateIdState(_id, state):
    datalist = []
    dic = {}
    dic['doc'] = {'type': state}
    datalist.append([_id, dic])
    updateBulk('cubist_naver_sid', datalist)


s = time.time()

try:
    
    qurey = {"query":{"bool":{"must":[{"match_all":{}}],"must_not":[],"should":[]}},"from":0,"size":1000,"sort":[],"aggs":{}}
    keyword_arr = getdetails_qurey('cubist_naver_keyword', qurey, esUrl = esUrl)
        
    keyword_dic = {}
    keyword_new_dic = {}
    keyword_company_dic = {}
    for _arr in keyword_arr:
        keyword_dic[_arr['_source']['value']] = _arr['_source']['type']
        keyword_new_dic [_arr['_source']['value']] = _arr['_source']['state']
        keyword_company_dic[_arr['_source']['state']] = _arr['_source']['keyword']
          
    
#    qurey = {"query":{"bool":{"must":[{"match_all":{}}],"must_not":[],"should":[]}},"from":0,"size":1000,"sort":[{'date':'desc'}],"aggs":{}}
    qurey = {"query":{"bool":{"must":[{"match":{"state":"False"}}],"must_not":[],"should":[]}},"from":0,"size":100,"sort":[{'date':'desc'}],"aggs":{}}
    id_arr = getdetails_qurey('cubist_naver_id', qurey, esUrl = esUrl)
    

    for idx, _arr in enumerate(id_arr):
        _arr = _arr['_source']
        
        d_id = ''
        d_id = _arr['id']
        #d_id = ded_id
        _nicName = _arr['value']
        _keywordNum = keyword_dic.get(_arr['keyword'], '')
        _keyword = keyword_new_dic.get(_arr['keyword'])
        _company = keyword_company_dic.get(_keyword)
        _type = _arr['type']
        
        
        # qurey = {"query":{"bool":{"must":[{"match_all":{}}],"must_not":[],"should":[]}},"from":0,"size":1000,"sort":[],"aggs":{}}
        qurey = {"query":{"bool":{"must":[{"match":{"type.keyword":_company}}],"must_not":[],"should":[]}},"from":0,"size":1000,"sort":[],"aggs":{}}
        message_arr = getdetails_qurey('cubist_naver_message', qurey, esUrl = esUrl)
            
        message_list = []
        for _arr in message_arr:
            message_list.append(_arr['_source']['value'])
        
        
        #렌덤으로 문장 생성
        b = random.randrange(0, len(message_list))
        s_message = message_list[b]
        s_message = s_message.replace('<Memo>', ' ')
        s_message = s_message.replace('<Type>', _type).replace('<Name>', _nicName).replace('<Keyword_num>', _keywordNum).replace('<Keyword>', _keyword).replace('<S>', '\n')
        
        # break
        ##보내기
        subject = _nicName+"님 협찬 제안 메일 송부 드려요!"
        
        sender_id = 'cubistmaster@gmail.com'
        pw = 'cleihlqyyxpdcjgy'
        
        # resiver = d_id+'@naver.com'
        resiver = 'iriyakana@naver.com'
        recipients = [resiver]
        password = pw
        
        send_email(subject, s_message, sender_id, recipients, password)
        
        ## es에 넣기
        _datalist = []
        _id = d_id #+ str(idx)
        TimeString, TimeValue = DateToString2('now')
        dic = {}
        dic['id'] = _id
        dic['value'] = s_message
        # 네이버 쪽지는 True
        # dic['state'] = 'True'
        dic['state'] = 'EMAIL'
        dic['date'] = TimeString
        dic['date2'] = TimeValue
        dic['keyword'] = subject
    #        dic['type'] = _type
        
        _datalist.append([_id, dic])
        
        insertBulk(_datalist, 'cubist_naver_smessage', esUrl)
        
        time.sleep(1)
        ## 블로거 아이디 쪽지 보냄 표시 필요
        makeLog('google', str(idx+1), d_id, 'ING')
        time.sleep(1)
        
        datalist = []
        dic = {}
        dic['doc'] = {'state':'True'}
        datalist.append([d_id, dic])
        updateBulk('cubist_naver_id', datalist)
        
        break
    
    print('all send time :',time.time() - s)
    
except Exception as E:
    print(E)
    makeLog('google', str(E), d_id, 'ERROR')
    time.sleep(1)
    # updateIdState(IDtoIndex[id], 'Block')
    
       
        
#        if str(E).find('하루에 보낼 수 있는 쪽지 50개를 모두 발송하셨습니다.') != -1:
#            
            
            ##update
            ##
#            
#            가장 마지막에 보낸 시간
#            오늘 가장 마지막에 보낸 횟수 
#            에러 메시지 ??
#        
#        
##        datalist = []
##        for i in range(3):
##            dic = {}
##            dic['doc'] = {:}
##            datalist.append([id, dic])
##        
##        
##        updateBulk('cubist_naver_sid', datalist):
#
#이걸 업데이트 하는 것이 나을까 ??
#아니면 데이터를 다시 쌓는게 나을까??
#로그라는 이름의 데이터를 다시 쌓기??
#
#셀렉티드 아이디
#로그 
#
#가장 최근 아이디가 에러 이면 다른아이디로

            
            


























#검색어 == 디바이스 매칭이 1:1 이 아닌 경우 URL이랑 어떻게 해야할지 선정
#하루에 몇개 정도 쪽지를 보낼 것인지
#아이디가 막히면... 찾을 로직 필요














#
#
#
#
#
#
#allCount = 0
#ipAddr = ''
#timer = ''
#
#
#  # if text != getText:
#        # text = getText
#        # #listout.append(text)
#        # f = open('url_tracer_output.csv', 'a', newline='', encoding='utf-8')
#        # wr = csv.writer(f)
#        # wr.writerow([text])
#        # outTime = time.time() - s
#        # wr.writerow([outTime])
#        # s = time.time()        
#        # print(text)
#        # f.close()
#
#
#
#words = readCsv('../keyword.txt')
#print('검색어 :', words)
#
#if words[0][0].find('auto')!= -1:
#    print('auto mode start')
#
#    q = {"query":{"bool":{"must":[{"match_all":{}}],"must_not":[],"should":[]}},"from":0,"size":1000,"sort":[],"aggs":{}}
#    r_arr = getdetails_qurey('cubist_naver_keyword', q)
#    
#    _temp = []
#    
#    for _arr in r_arr:
#        _arr = _arr['_source']
#        _temp.append([_arr['value']])
#
#    words = _temp
#    print('검색어 :', words)
#
#
#try:
#    size = readCsv('./size.txt')
#except:
#    size = readCsv('../size.txt')
#
#size = int(size[0][0])
#print('검색 사이즈 :', size)
#
#try:
#    message = readCsv('./message.txt')
#except:
#    message = readCsv('../message.txt')
#
#text = ''
#for _m in message:
#    text += (_m[0])
#
#
#overTime = len(words) * 2 * size
#
### get id list
#q = {"query":{"bool":{"must":[{"match_all":{}}],"must_not":[],"should":[]}},"from":0,"size":1000,"sort":[],"aggs":{}}
#r_arr = getdetails_qurey('cubist_naver_id', q)
#    
#ed_id_list = []
#for _arr in r_arr:
#    _arr = _arr['_source']
#    ed_id_list.append(_arr['id'])
#
##if timer != '': 
##    timer.cancel()
##
##timer = threading.Timer(overTime, overTimer)
##timer.start()
#
#
#
##driver = webdriver.Chrome()
#
#for word in words:
#    word = word[0]
#    print(word)
#    
#    
#    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='+word
#    driver.get(url)
#
#    for _ in range(3):
#        ActionChains(driver).send_keys(Keys.END).perform()
#        time.sleep(0.5)
#
#
#     
#    html = driver.page_source
#    soup = BeautifulSoup(html, 'html.parser')
#    #numList = soup.find_all(class_= 'api_more_wrap')
#    numList = soup.find_all('a')
#
#
#    clickList = readCsv('../search.txt')
#    #clickList = ['후기 더보기','참여 콘텐츠 더보기','팁 모음 더보기']
#
#
#    _urlList = []
#
#    for num in numList:
##        num = num.findNext('a')
#        for click in clickList:
#            if str(num.getText()).find(click[0]) != -1:
#                if str(num['href']).find('https://in.naver.com/') == -1:
#                    _urlList.append(num['href'])
#                #xpath = xpath_soup(num)
#                #selenium_element = driver.find_element_by_xpath(xpath)
#                #    ActionChains(driver).move_to_element(selenium_element).perform()
#                #   selenium_element.click()
#                 
#                    time.sleep(0.5)
#                
#                
##    for _url in _urlList:
##    
##        if str(_url)[0] == '?':
##            _url = 'https://search.naver.com/search.naver'+_url
##        
##        driver.get(_url)
##        
##        html = driver.page_source
##        soup = BeautifulSoup(html, 'html.parser')
##        numList = soup.find_all(class_= 'group_inner')
##        
##        for num in numList:
##            #print(num.findNext('a').getText(), num.findNext('a')['href'], str(num.findNext('a')['href']).replace('https://','').split('/')[1])
##            f = open('../result_'+DateToString('now')+'.txt', 'a', newline='', encoding='utf-8')
##            wr = csv.writer(f)
##            wr.writerow([word, num.findNext('a').getText(), num.findNext('a')['href'], str(num.findNext('a')['href']).replace('https://','').split('/')[1]])
##            f.close()
#
#    NaverIDtoBlog_all = {}
#    NaverIDtoIn_all = {}
#    
#    for _url in _urlList:
#    
#        if str(_url)[0] == '?':
##            _url = 'https://search.naver.com/search.naver'+_url
#        #모바일
#            _url = 'https://m.search.naver.com/search.naver'+_url
#        driver.get(_url)
#        
#        for _ in range(5):
#            ActionChains(driver).send_keys(Keys.END).perform()
#            time.sleep(1)
#        
#        html = driver.page_source
#        soup = BeautifulSoup(html, 'html.parser')
#        numList = soup.find_all('a')
#        
#        getNaverIDtoIn = []
#        getNaverIDtoBlog = []
#        
#        except_words = ['naver_search', 'MyBlog.naver', 'nidlogin.login', 'influencer_search', 'nidlogin.login', 'challenge']
#        
#        for num in numList:
#            try:
#                if str(num['href']).find('https://in.naver.com/') != -1:
##                    for _word in except_words:
##                        if str(num['href']).find(_word) == -1:
#                    getNaverIDtoIn.append(num['href'])
#                
##                if str(num['href']).find('https://blog.naver.com/') != -1:
#                if str(num['href']).find('blog.naver.com/') != -1:
#                    getNaverIDtoBlog.append(num['href'])
#                    
#                    
##                if str(num['href']).find('https://blog.naver.com/') != -1:
##                    getNaverIDtoBlog.append(num['href'])
#            except:
#                pass
#        
#        
#        NaverIDtoBlog = {}
#        for _idLink in getNaverIDtoBlog:
#            isExceptWord = False
#            for _word in except_words:
#                if str(_idLink).find(_word) != -1:
#                    isExceptWord = True
#                    break
#            if isExceptWord:
#                continue
#        
#            _id = str(_idLink).replace('https://','').split('/')[1]
#            
#            NaverIDtoBlog[_id] = 1
#            
#            if len(NaverIDtoBlog) >= size:
#                break
#        
#
#        NaverIDtoIn = {}
#        for _idLink in getNaverIDtoIn:
#            isExceptWord = False
#            for _word in except_words:
#                if str(_idLink).find(_word) != -1:
#                    isExceptWord = True
#                    break
#            if isExceptWord:
#                continue
#            
##            if str(_idLink).find('?query') != -1:
##                continue
#            
#            _id = str(_idLink).replace('https://','').split('/')[1].split('?')[0]
#            
#            NaverIDtoIn[_id] = 1
#            
#            if len(NaverIDtoIn) >= size:
#                break
#        
#        
#        ##여기에 중복제거 로직 추가
#        for __ID in NaverIDtoIn.keys():
#            NaverIDtoIn_all[__ID] = 1
#            
#        for __ID in NaverIDtoBlog.keys():
#            NaverIDtoBlog_all[__ID] = 1
#
#        
#    #블로그를 탐색하며 실 ID 체크 및 NICNAME 체크  
#    datalist = []
#    for k in NaverIDtoBlog_all.keys():
#        if k == '':
#            continue
#        
#        # es id 있으면 넘기기
#        if k in ed_id_list:
#            continue
#        
#        dic = {}
#        dic['keyword'] = word
#        try:
#            _type = '블로거'
#            __url = 'https://blog.naver.com/'+k
#            driver.get(__url)
#            dic['id'] = k
#            dic['type'] = _type
#            
##                driver.switch_to.frame('mainFrame')
##                _name = driver.find_element_by_xpath('//*[@id="nickNameArea"]').text
##                dic['name'] = _name
#            
#            _name = getMobileBlogNic()
#            if _name == -1:
#                continue
#            
#            dic['name'] = str(_name).replace('마켓블로그','').replace('공식 블로그','')
#            
#            datalist.append(dic)
#            
#            
#            _datalist = []
#            _id = k
#            TimeString, TimeValue = DateToString2('now')
#            dic = {}
#            dic['id'] = _id
#            dic['value'] = _name
#            dic['state'] = 'False'
#            dic['date'] = TimeString
#            dic['date2'] = TimeValue
#            dic['keyword'] = word
#            dic['type'] = _type
#            
#            _datalist.append([_id, dic])
#            
#            insertBulk(_datalist, 'cubist_naver_id', esUrl)
#            
#            
#            
#            f = open('../result_'+DateToString('now')+'.txt', 'a', newline='', encoding='utf-8')
#            wr = csv.writer(f)
#            wr.writerow([word, k, _type, _name])
#            f.close()
#            
#            sendText = text.replace('{{ID}}', k).replace('{{Type}}', _type).replace('{{Name}}', _name)
#            
#            f = open('../result_form_'+DateToString('now')+'.txt', 'a', newline='', encoding='utf-8')
#            wr = csv.writer(f)
#            wr.writerow([sendText])
#            f.close()
#            
#            time.sleep(0.7)
#        except:
#            pass
#        
#    
#    for k in NaverIDtoIn_all.keys():
#        
#        if k in list(NaverIDtoBlog_all.keys()):
#            continue
#            
#        if k == '':
#            continue
#        
#        # es id 있으면 넘기기
#        if k in ed_id_list:
#            continue
#        
#        dic = {}
#        dic['keyword'] = word
#        try:
#            
#            _type = '인플루언서'
#            __url = 'https://blog.naver.com/'+k
#            driver.get(__url)
#            dic['id'] = k
#            dic['type'] = _type
#            
##                driver.switch_to.frame('mainFrame')
##                _name = driver.find_element_by_xpath('//*[@id="nickNameArea"]').text
##                dic['name'] = _name
#            
#            _name = getMobileBlogNic()
#            if _name == -1:
#                continue
#            
#            dic['name'] = str(_name).replace('마켓블로그','').replace('공식 블로그','')
#            
#            datalist.append(dic)
#            
#    
#            _datalist = []
#            _id = k
#            TimeString, TimeValue = DateToString2('now')
#            dic = {}
#            dic['id'] = _id
#            dic['value'] = _name
#            dic['state'] = 'False'
#            dic['date'] = TimeString
#            dic['date2'] = TimeValue
#            dic['keyword'] = word
#            dic['type'] = _type
#            
#            _datalist.append([_id, dic])
#            
#            insertBulk(_datalist, 'cubist_naver_id', esUrl)
#            
#            
#            f = open('../result_'+DateToString('now')+'.txt', 'a', newline='', encoding='utf-8')
#            wr = csv.writer(f)
#            wr.writerow([word, k, _type, _name])
#            f.close()
#            
#            sendText = text.replace('{{ID}}', k).replace('{{Type}}', _type).replace('{{Name}}', _name)
#            
#            f = open('../result_form_'+DateToString('now')+'.txt', 'a', newline='', encoding='utf-8')
#            wr = csv.writer(f)
#            wr.writerow([sendText])
#            f.close()
#            
#            time.sleep(0.7)
#            
#        except:
#            pass
#        
#
#
#
##<a target="_blank" href="https://in.naver.com/iamchocolat?query=%EB%AF%B8%EC%8A%A4%ED%8A%B8+%EC%B0%B8%EC%97%AC+%EC%BD%98%ED%85%90%EC%B8%A0" class="name" onclick="goOtherCR(this, 'a=itb_bas*f.profile&amp;r=19&amp;i=SPC-0000000000006816.a0209rl4_nblog_post_222653959305&amp;g=%7B%22bid%22%3A%22SPC-0000000000006816%22%2C%22docRank%22%3A1%7D&amp;u='+urlencode(this.href));">쇼콜라</a>
##        <a target="_blank" href="https://in.naver.com/cosreader?query=%EB%B7%B0%EB%9F%AC" class="name elss" onclick="return goOtherCR(this,'a=ink_kib*a.nickname&amp;r=1&amp;i=a0209rl4_nblog_post_222652147919&amp;u='+urlencode(this.href))"><span class="txt">화장품읽어주는남자</span></a>
##        
#        
#driver.close()   
#        
#        
#        # outTime = time.time() - s
#        # wr.writerow([outTime])
#        # s = time.time()        
#        # print(text)
#        
#        
#        
#        
#        # if num.findNext('a')['href'] == '#':
#            # num = num.findNext('a')
#            # print(num.findNext('a')['href'])
#        # else:
#            # print(num.findNext('a')['href'])
#    
#
#
#
#
#
#
## html = driver.page_source
## soup = BeautifulSoup(html, 'html.parser')
## numList = soup.find_all(class_= 'api_more_wrap')
#            
## while(True):
#    # if string == str(nextNum.getText()):
#        # break
#    # nextNum = nextNum.findNext('a')
#
## xpath = xpath_soup(nextNum)
## selenium_element = driver.find_element_by_xpath(xpath)
## #    ActionChains(driver).move_to_element(selenium_element).perform()
## selenium_element.click()
#
#        # #print(driver.title)
#        
#        # timer = threading.Timer(1201, overTimer)
#        # timer.start()
#
#        # time.sleep(2)
#        # driver.get("https://naver.com")
#        
        
        

            
            
            
            
            
            
        

