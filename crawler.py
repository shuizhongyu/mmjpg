#coding:utf-8



#将模板重新用于99mm



import requests
from bs4 import BeautifulSoup
from urllib import request
import os
import re
from multiprocessing import Process

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
        #f = open('./out.txt','w')
        #f.write(r2.text)
        #f.close()
        soup2 = BeautifulSoup(r2.text)
        t2 = soup2.find('div',id="picbox")
        #print(t2.find('img').get('src'))
        request.urlretrieve(t2.find('img').get('src').strip(),path+'/'+str(i)+'.jpg')

def getimglink(base_url,url,path):
    r = requests.get(url)
    #解决乱码
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text)

    x = 1
    for img in soup.find_all('a',attrs={"target":"_blank"}):
        #print('!!!!!!!')
        #print(img.get('href'))
        image_url = base_url + str(img.get('href'))
        #这样查出来的标签有一个是下面的标题，是多余的
        if img.find('img')== None:
            continue
        name = img.find('img').get('alt')
        #print("name:"+name+"!!!!!!!!!")
        #创建文件夹
        if not os.path.exists(path+name):
            os.makedirs(path+name)
        getimg(base_url,image_url,path+name)
        x += 1
        #request.urlretrieve(image_url.strip(),'./pic/%s.jpg' % x)


if __name__ == '__main__':


    base_url = 'http://www.99mm.me/'
    #抓几页，每页10个
    page = 1
    path = './99mm/'
    url=base_url
    for p in range(1,page+1):
        if(page == 1):
            getimglink(base_url,url,path)
        else:
            url = base_url + '/hot/mm_4_'+str(page)+'.html'
            getimglink(base_url,url,path)

