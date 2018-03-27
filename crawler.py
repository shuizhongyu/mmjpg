#coding:utf-8




#套用到另一个类似网站上，并修改函数


import requests
from bs4 import BeautifulSoup
from urllib import request
import os
import re

def getimg(base_url,url,path):
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    "Host:": "192.168.1.1",
    "Connection":"close",
    "Accept-Encoding": "identity",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}
    #print(url)
    r = requests.get(url,headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text)

    #获取总页码
    temp = soup.find('div',id='fenye').find('li').text
    total = int(re.findall("\d+",temp)[0])
    #print(soup.prettify())
    #print("total:"+str(total)+"!!!!!!!!")

    t = soup.find('a',href="javascript:dPlayNext();")
    request.urlretrieve(base_url+t.find('img').get('src').strip(),path+'/'+'1.jpg')
    if total<=1:
        return
    for i in range(2,total+1):
        url2 = url + '?url=' + str(i)
        r2 = requests.get(url2,headers)
        r2.encoding = 'utf-8'
        f = open('./out.txt','w')
        f.write(r2.text)
        f.close()
        soup2 = BeautifulSoup(r2.text)
        t2 = soup2.find('a',href="javascript:dPlayNext();")
        #print(t2.find('img').get('src'))
        request.urlretrieve(base_url+t2.find('img').get('src').strip(),path+'/'+str(i)+'.jpg')

def getimglink(base_url,url,path):
    r = requests.get(url)
    #解决乱码
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text)

    x = 1
    for img in soup.find_all('a',attrs={"target":"_blank"}):
        #print('!!!!!!!')
        #print(img.get('href'))
        image_url = str(img.get('href'))
        #这样查出来的标签有一个是下面的标题，是多余的
        if img.find('img')== None:
            continue
        name = img.find('img').get('alt')
        #print("name:"+name+"!!!!!!!!!")
        #创建文件夹
        if not os.path.exists(path+name):
            os.makedirs(path+name)
        getimg(baseurl,image_url,path+name)
        x += 1
        #request.urlretrieve(image_url.strip(),'./pic/%s.jpg' % x)


if __name__ == '__main__':


    base_url = 'http://www.93xmn.com/'
    #抓几页，每页10个
    page = 1
    path = './94xmn/'
    url=base_url
    for p in range(1,page+1):
        if(page == 1):
            getimglink(base_url,url,path)
        else:
            url = base_url + 'xingganmeinv/list_2_'+str(page)+'.html'
            getimglink(base_url,url,path)

