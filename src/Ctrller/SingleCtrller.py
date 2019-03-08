#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

This program can scrape liked users for one photo and output them to one file.

Author: JeffXu
Last edited: Feb 2019
"""

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import openpyxl
import math
import sys
#import csv
import os
import time

sys.path.append('./Util/')
import ScrapeUtil
import BaseUtil
sys.path.append('./Model/')
import User

class Ctrller(object):
    def __init__(self):       
        self.sizeOfOnePage = 100

    def setPhotoId(self, photoId):
        self.photoId = photoId

    def setOutputPath(self, path):
        self.outputPath = path

    def addUsersOnePage(self, users, photoId, pageIndex, sizeOnePage):
        likedUsersJson =  ScrapeUtil.getLikedUsersJsonTpl(photoId, pageIndex, sizeOnePage)
        response = urlopen(likedUsersJson).read().decode('utf-8')
        responseJson = json.loads(response)
        print(pageIndex, " ", len(responseJson.get("pictureLikeeds")))
        for uJson in responseJson.get("pictureLikeeds"):
            print(uJson.get('nickName'))
            user  = User.make_User(uJson.get('nickName'), uJson.get('id'))
            users.append(user)

    def addUsersPages(self, users, photoId, numOfPages, sizeOnePage):
        for i in range(numOfPages):
            self.addUsersOnePage(users, photoId, i + 1,sizeOnePage)
            #print(len(users), " ", i)
        
    def start2Scrape(self):
        driver = webdriver.PhantomJS(executable_path=ScrapeUtil.phantomjsUrl)
        driver.get(ScrapeUtil.getPhotoPageUrl(self.photoId))
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "content")))
        except:
            print("Oops!",sys.exc_info()[0],"occured.")
        finally:
            pageSource = driver.page_source
            driver.close()
            bsObj = ScrapeUtil.getBSObjByHTML(pageSource)
            totalLikedNum = int(bsObj.find(class_="v2_new_fav with_count").find("span", {"class":"value"}).get_text())
            photoName = bsObj.find(id="content").h2.get_text()
            users = []
            if totalLikedNum > 0:
                numOfPages = math.ceil(totalLikedNum / self.sizeOfOnePage)
                print(totalLikedNum)
                print(numOfPages)
                self.addUsersPages(users, self.photoId, numOfPages, self.sizeOfOnePage)
                print("length is", len(users))

        """
        with open('./test.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['PhotoName', 'Num', 'NickNames', 'Links'])
            if totalLikedNum == 0:
                writer.writerow([photoName, totalLikedNum])
            else:
                for i in range(len(users)):
                    if i == 0:
                        writer.writerow([photoName, totalLikedNum, users[i].nickName, ScrapeUtil.getUserPageUrlTpl(users[i].userId)])
                    if i > 0:
                        writer.writerow(['', '', users[i].nickName, ScrapeUtil.getUserPageUrlTpl(users[i].userId)])
        """
        path = self.outputPath
        if os.path.exists(path):
            os.remove(path)
        mywb = openpyxl.Workbook()
        mysheet = mywb['Sheet']
        if totalLikedNum == 0:
            BaseUtil.writerow2xl(mysheet, 1, [photoName, totalLikedNum])
        else:
            for i in range(len(users)):
                j = i + 1
                if j == 1:
                    BaseUtil.writerow2xl(mysheet, j, [photoName, totalLikedNum, users[i].nickName, ScrapeUtil.getUserPageUrlTpl(users[i].userId)])                
                if j > 1:
                    BaseUtil.writerow2xl(mysheet, j, ['', '', users[i].nickName, ScrapeUtil.getUserPageUrlTpl(users[i].userId)])
                mysheet.cell(row=j, column=3).hyperlink = ScrapeUtil.getUserPageUrlTpl(users[i].userId)
        mywb.save(path)
        
#for unit test

"""  
if __name__ == '__main__':
    print(f"started at {time.strftime('%X')}")
    ctrller = Ctrller()
    ctrller.setPhotoId("673b1757dbab43dd80505ac845f9b3b8")
    ctrller.setOutputPath("../../output")
    ctrller.start2Scrape()
    print(f"end at {time.strftime('%X')}")
"""

