# coding: utf-8

from bs4 import BeautifulSoup
import requests
import json
import os

SLACK_URL = os.environ['SLACK_URL']
WANTED_DOMAIN = os.environ['WANTED_DOMAIN']

response = requests.post(
    'https://secure.sakura.ad.jp/signup2/domain.php',
    {'domain': WANTED_DOMAIN,
     'tld[com]': 1,
     'tld[org]': 0,
     'tld[net]': 0,
     'tld[info]': 0,
     'tld[biz]': 0,
     'tld[jp]': 0,
     })

html = response.text.encode(response.encoding)
soup = BeautifulSoup(html, "html.parser")
domain = soup.select('div.domain-search-results')[0].th.font.string
comment = soup.select('div.domain-search-results')[0].td.font.string

if comment != '取得できません':
    response = requests.post(
        SLACK_URL,
        json.dumps({'text': 'さくらドメインの ' + domain + ' を探したよ〜！\nステータス :  `' + comment + '`',
                    "username": "miss-suzuki.comを監視するマン",
                    "channel": "#general",
                    }),
        headers={'Content-Type': 'application/json'})

