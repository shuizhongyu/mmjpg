#coding:utf-8



#实现以文件夹为单位怕套图，但所有的都是第一张图片


import requests
from bs4 import BeautifulSoup
from urllib import request
import os
import re

def getimg(url,path):
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
    temp = soup.find('div',{"class":"column"}).find('span').text
    total = int(re.findall("\d+",temp)[0])
    #print(soup.prettify())
    #print("total:"+str(total)+"!!!!!!!!")

    t = soup.find('div',id="picbox")
    request.urlretrieve(t.find('img').get('src').strip(),path+'/'+'1.jpg')
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
        t2 = soup2.find('div',id="picbox")
        print(t2.find('img').get('src'))
        request.urlretrieve(t2.find('img').get('src').strip(),path+'/'+str(i)+'.jpg')

def getimgfolder(url,path):
    r = requests.get(url)
    #解决乱码
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text)

    x = 1
    for img in soup.find_all('a',attrs={"target":"_blank"}):
        #print('!!!!!!!')
        #print(img.get('href'))
        image_url = 'http://www.99mm.me'+str(img.get('href'))
        #print('img:'+img.find('img').get('alt')+"!!!!!!")
        #这样查出来的标签有一个是下面的标题，是多余的
        if img.find('img')== None:
            continue
        name = img.find('img').get('alt')
        #print("name:"+name+"!!!!!!!!!")
        #创建文件夹
        path = path+name
        if not os.path.exists(path):
            os.makedirs(path)
        getimg(image_url,path)
        x += 1
        #request.urlretrieve(image_url.strip(),'./pic/%s.jpg' % x)


if __name__ == '__main__':


    url = 'http://www.99mm.me'
    #抓几页，每页10个
    page = 1
    path = './99mm/'
    for p in range(1,page+1):
        if(page == 1):
            getimgfolder(url,path)
        else:
            url2 = url + '/hot/mm_4_'+str(page)+'.html'
            getimgfolder(url2,path)

