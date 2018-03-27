#coding:utf-8



#17786
#成功了，终于在一个网站成功了，证明以前的都是网站做了限制
#我的多进程好像用错地方了，需要修改
#应该是抓每个图集一个进程，而不是抓每页的所有图集一个进程
#之前的多进程设置多页时是有作用的
#已修改为每个图集一个进程
#效果显著，一下子出现很多文件夹


#跑了一晚上试了一下，抓到200+M图片
#其实在跑的前两个小时已经抓了这么多了
#后面虽然链接一直在，但没抓到东西

import requests
from bs4 import BeautifulSoup
from urllib import request
import os
import re
from multiprocessing import Pool

def getimg(base_url,url,path):
    headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36',
    "Host:": "192.168.1.1",
    "Connection":"keep-alive",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer":"http://www.17786.com"
}
    #print(url)
    r = requests.get(url,headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text)

    #获取总页码
    total = 10
    #print(soup.prettify())
    #print("total:"+str(total)+"!!!!!!!!")

    t = soup.find('div',id="picBody")
    request.urlretrieve(t.find('img').get('src').strip(),path+'/'+'1.jpg')
    if total<=1:
        return
    for i in range(2,total+1):
        url2 = url[0:-5] + '_' + str(i) + ".html"
        r2 = requests.get(url2,headers)
        r2.encoding = 'utf-8'
        #f = open('./out.txt','w')
        #f.write(r2.text)
        #f.close()
        soup2 = BeautifulSoup(r2.text)
        t2 = soup2.find('div',id="picBody")
        #print(t2.find('img').get('src'))
        request.urlretrieve(t2.find('img').get('src').strip(),path+'/'+str(i)+'.jpg')

def getimglink(base_url,url,path,pool):
    headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36',
    "Host:": "192.168.1.1",
    "Connection":"keep-alive",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer":"http://www.17786.com"
}

    r = requests.get(url,headers)
    #解决乱码
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text)

    x = 1
    for img in soup.find_all('a',attrs={"target":"_blank"}):
        #print('!!!!!!!')
        #print(img.get('href'))
        image_url = base_url + str(img.get('href'))[16:]
        #这样查出来的标签有一个是下面的标题，是多余的
        if img.find('img')== None:
            continue
        name = img.find('img').get('alt')
        #print("name:"+name+"!!!!!!!!!")
        #创建文件夹
        if not os.path.exists(path+name):
            os.makedirs(path+name)

        pool.apply_async(getimg,(base_url,image_url,path+name))
        #getimg(base_url,image_url,path+name)
        x += 1
        #request.urlretrieve(image_url.strip(),'./pic/%s.jpg' % x)


if __name__ == '__main__':


    base_url = 'http://www.17786.com/ent/meinvtupian/'
    #抓几页，每页10个
    page = 20
    path = './mmjpg/'
    url = base_url

    #多进程
    process = 8
    pool = Pool(process)
    for p in range(1,page+1):
        if(p == 1):
            getimglink(base_url,url,path,pool)

            #pool.apply_async(getimglink,(base_url,url,path))
        else:
            url = base_url + '/index_' + str(page) + ".html"

            getimglink(base_url,url,path,pool)

            #pool.apply_async(getimglink,(base_url,url,path))

    pool.close()
    pool.join()



