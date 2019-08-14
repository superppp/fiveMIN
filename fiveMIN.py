# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime
import requests

tmp = datetime.date.today()
today = tmp.strftime('%Y%m%d')
html = 'https://www.twse.com.tw/exchangeReport/MI_5MINS?response=html&date='+today
head_html = urlopen(html).read().decode("utf-8")
if datetime.datetime.now().strftime('%H%M') > '1330':
    a=((head_html.split('</tbody>')[0]).split('<td>')[-1]).split('</td>')[0]
else:
    a = 'No Data'
print('每5秒委託成交統計: ', a)

html = 'https://www.taifex.com.tw/cht/3/futContractsDate'
head_html = urlopen(html).read().decode("utf-8")
a = head_html.split('12bk')[6]
soup = BeautifulSoup(a, 'html.parser')
fontall = soup.find_all('font')
print('外資未平倉: ', fontall[-1].string.strip())
print('外資未平倉多單: ', fontall[-3].string.strip())
print('外資未平倉空單: ', fontall[-2].string.strip())
print('')
b = head_html.split('12bk')[15]
soup = BeautifulSoup(b, 'html.parser')
fontall = soup.find_all('font')
print('小臺外資未平倉多單: ', fontall[-3].string.strip())
print('小臺外資未平倉空單: ', fontall[-2].string.strip())

c = head_html.split('12bk')[14]
soup = BeautifulSoup(c, 'html.parser')
fontall = soup.find_all('font')
print('小臺投信未平倉多單: ', fontall[-3].string.strip())
print('小臺投信未平倉空單: ', fontall[-2].string.strip())

d = head_html.split('12bk')[13]
soup = BeautifulSoup(d, 'html.parser')
fontall = soup.find_all('font')
print('小臺自營商未平倉多單: ', fontall[-3].string.strip())
print('小臺自營商未平倉空單: ', fontall[-2].string.strip())

today = tmp.strftime('%Y/%m/%d')
html = 'https://www.taifex.com.tw/cht/3/futDailyMarketReport'
mypara = {'commodity_id':'MTX', 'commodity_idt':'MTX', 'marketCode':'0', 'MarketCode':'0', 'questDate':today, 'queryType':'2'}
re = requests.post(html, data=mypara)
str = re.text
strpar = str.split('MTX')[6]
a=strpar.split('</td>')[9]
print('小臺未平倉: ', a.strip().split('\t')[-1])

url = 'https://www.taifex.com.tw/cht/3/optDailyMarketSummaryExcel'
response = urlopen(url).read().decode("utf-8")
sp = BeautifulSoup(response, 'html.parser')
tbls=sp.find_all('table',attrs={'class':'table_a'})
tr1=tbls[0].find_all('tr')
tr2=tbls[1].find_all('tr')
tr1td = []
tr2td = []
for i in tr1[1:-2]:
    tr1td.append(i.find_all('td'))
for i in tr2[1:-2]:
    tr2td.append(i.find_all('td'))
tr1tdBuy = []
tr1tdSell = []
for i in tr1td:
    tr1tdBuy.append([j.text.strip() for j in i])
for i in tr2td:
    tr1tdSell.append([j.text.strip() for j in i])

fairPrice = []
for i in range(len(tr1tdSell)):
    if tr1tdBuy[i][5] == '-' and tr1tdSell[i][5] == '-':
        fairPrice.append(9999)
    else:
        a = abs(float(tr1tdBuy[i][5]) - float(tr1tdSell[i][5]))
        fairPrice.append(a)
print('')

weektoday = datetime.date.today().weekday()
if weektoday == 3:
    opType = 2
else:
    opType = 3
for i in range(opType):
    a = fairPrice.index(min(fairPrice))
    fairPrice[a] = 9999
    print(tr1tdBuy[a][0], tr1tdBuy[a][1], 'B:', tr1tdBuy[a][5], 'P:', tr1tdSell[a][5])