#coding:utf-8



#修改多进程为进程池
#htop中有7个进程在跑
#有多进程效果，应该是受网络连接数限制了，应该是和网站有关
#在程序运行后，net -nat中连接数量一直在增加
#每下一个图片就会建一个连接？
#这会导致连接过多从而被网站限制？


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
    "Referer":"http://www.99mm.me"
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
    headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36',
    "Host:": "192.168.1.1",
    "Connection":"keep-alive",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

    r = requests.get(url,headers)
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
    url = base_url

    #多进程
    process = 4
    pool = Pool(process)
    for p in range(1,page+1):
        if(page == 1):
            #getimglink(base_url,url,path)

            pool.apply_async(getimglink,(base_url,url,path))
        else:
            url = base_url + '/hot/mm_4_'+str(page)+'.html'
            #getimglink(base_url,url,path)

            pool.apply_async(getimglink,(base_url,url,path))

    pool.close()
    pool.join()



