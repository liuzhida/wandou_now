#!/usr/bin/env python
# -*-coding:utf-8-*-
#
# Author: liuzhida - zhida@wandoujia.com
# Blog: http://liuzhida.com
# Last modified: 2014-02-06 16:05
# Filename: test.py
# Description:
from BeautifulSoup import BeautifulSoup
import redis

c = redis.Redis(host='127.0.0.1', port=6379, db=0)

with open('1.html', 'r') as w:
    data = w.read()

soup = BeautifulSoup(data)
shops = soup.find('div', attrs={'class': 'shop_list'})
for shop in shops.findAll('li'):
    s = dict()
    name = shop.find('h6').string
    if not name:
        continue
    name = name.strip()
    print name

    link = shop.find('a')['href']
    id = link.lstrip(
        "javascript:window.location.href=").strip("'").lstrip("/shop/")
    print id

    link = "dianping://shopinfo?id=" + id

    star = shop.find('div', attrs={'class': 'comment-rst'}).find("span")['class']
    star = star.lstrip("item-rank-rst irr-star")
    print star

    _tags = shop.find('div', attrs={'class': 'desc'}).findAll("span")
    tags = list()
    for tag in _tags:
        tag = tag.string
        tags.append(tag)
        print tag

    distance = shop.find('span', attrs={'class': 'distance'}).string
    print distance

    s['link'] = link
    s['name'] = name
    s['id'] = id
    s['tags'] = tags
    s['distance'] = distance
    s['star'] = star
    c.hmset("shop:%s"%id, s)
    c.lpush("shoplist","shop:%s"%id)
