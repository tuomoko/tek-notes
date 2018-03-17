#!/usr/bin/env python2
# -*- coding: utf-8 -*-
u"""Downloads notes from the TEK web.

@author: Tuomo Kohtamäki
"""
import requests
from bs4 import BeautifulSoup
import os.path
import wget
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

url_root = 'https://teknet.tek.fi/arkisto.lehti/content/'
url = url_root+'ack-vad-gul.html'

r = requests.get(url, verify=False)
parsed_html = BeautifulSoup(r.text, 'lxml')
songs = parsed_html.body.find('ul', attrs={'class': 'blog-list'})
song_urls = songs.find_all('a')
urls = map(lambda x: x.get('href'), song_urls)
# names = map(lambda x: x.string, song_urls)

for song_url in urls:
    correct_url = song_url.replace("a%CC%88", "%C3%A4")
    correct_url = correct_url.replace("o%CC%88", "%C3%B6")
    r_song = requests.get(url_root+correct_url, verify=False)
    parsed_html = BeautifulSoup(r_song.text, 'lxml')
    content = parsed_html.body.find('div', attrs={'class': 'node'})
    if content:
        imgs = content.find_all('img')
        img_urls = map(lambda x: x.get('src'), imgs)
        for img_url in img_urls:
            filename = img_url[img_url.rfind("/")+1:]
            if not os.path.isfile(filename):
                wget.download(url_root+img_url)
