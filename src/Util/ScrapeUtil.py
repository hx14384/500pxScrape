#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

This program offers tool files for scraping.
Author: JeffXu
Last edited: Feb 2019
"""

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re

photoPageUrlTpl = "https://500px.me/community/photo-details/{}"
userPageUrlTpl = "https://500px.me/community/user-details/{}"
likedUsersJsonTpl = "https://500px.me/community/res/relation/{}/liked?startTime=&page={}&size={}&type=json"
phantomjsUrl = './phantomjs-2.1.1-windows/bin/phantomjs'

def getBSObjByHTML(html):
    bsObj = BeautifulSoup(html, features="html.parser")
    if bsObj == None:
        print ("Warning! bsObj is None.")
        return None
    return bsObj

def getBSObjByURL(url):
    try : 
        html = urlopen( url)
        print(html.read())
    except HTTPError as e:
        print("HT TPError getting html failed.")
        return None
    return getBSObjByHTML(html)

def getPhotoPageUrl(photoId):
    return photoPageUrlTpl.format(photoId)

def getUserPageUrlTpl(userId):
    return userPageUrlTpl.format(userId)

def getLikedUsersJsonTpl(photoId, pageIndex, sizeOnePage):
    return likedUsersJsonTpl.format(photoId, pageIndex, sizeOnePage)
