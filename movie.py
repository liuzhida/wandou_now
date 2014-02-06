#!/usr/bin/env python
# -*-coding:utf-8-*-
#
# Author: liuzhida - zhida@wandoujia.com
# Blog: http://liuzhida.com
# Last modified: 2014-02-06 19:16
# Filename: movie.py
# Description: 
import requests
from BeautifulSoup import BeautifulSoup
import redis
c = redis.Redis(host='127.0.0.1', port=6379, db=0)


def header():
    header = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) CriOS/32.0.1700.20 Mobile/11B554a Safari/9537.53'}
    return header


#url = "http://api.flixster.com/iphone/api/v1/movies.json?&view=long&filter=popular&version=6.8.1&locale=en_US&country=us&osVersion=7.0.4&conn=6&deviceType=iPhone5&screenResolution=640x1136&udt=1128516710"
url = "http://movie.douban.com/nowplaying"
headers = header()
r = requests.get(url,headers=headers)
data = r.text


for i in c.keys("movielist"):
    print i
    c.delete(i)

soup = BeautifulSoup(data)
movies = soup.findAll('li', attrs={'data-category':'nowplaying'})
for m in movies:
    s = dict()
    s['name']     = m['data-title']
    s['score']    = m['data-score']
    s['star']     = m['data-star']
    s['actors']   = m['data-actors']
    s['duration'] = m['data-duration']
    s['id']       = m['id']
    s['director'] = m['data-director']
    s['img']      = m.find("img")['src']
    print s['name']
    c.hmset("movie:%s"%s['id'], s)
    c.lpush("movielist","movie:%s"%s['id'])
    

'''
data-score="7.0" data-star="35" data-release="2014" data-duration="108分钟" data-region="中国大陆" data-director="田羽生" data-actors="韩庚 / 姚星彤 / 郑恺" data-category="nowplaying" data-enough="True" data-showed="True" data-votecount="16554" data-subject="24751754"
'''

