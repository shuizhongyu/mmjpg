#coding:utf-8



#重新用到mmjpg，试试越过反盗链
#失败，再换网站
#成功，headers中host设为192.168.1.1的原因，删除后正常
#添加随机agent,依然不行
#独立获得网页函数
#爬了10页900+M
#可以再修改，爬完整个网站


import requests
from bs4 import BeautifulSoup
from urllib import request
import os
import re
import random
from multiprocessing import Pool


def geturl(url):
    headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36',
    "Host": "192.168.1.1",
    "Connection":"keep-alive",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}
    user_agent = [
    'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
    'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
    'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)'
    ]
    #设置网页编码格式，解码获取到的中文字符
    #构造http请求头，设置user-agent
    headers["User-Agent"] = random.choice(user_agent)
    headers["Referer"] = "http://www.mmjpg.com"

    try:
        #r = requests.get(url,headers = headers)
        r = requests.get(url)
        r.encoding = 'utf-8'
    except BaseException as e:
        print("exception:",e)
        return None

    return r

def downjpg(src,path):
    #存在不重新下载
    if not(os.path.exists(path)):
        print("download "+path)
    else:
        print("exists "+path)
        return

    headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36',
    "Connection":"keep-alive",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}
    user_agent = [
    'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
    'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
    'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)'
    ]
    #设置网页编码格式，解码获取到的中文字符
    #构造http请求头，设置user-agent
    #headers["User-Agent"] = random.choice(user_agent)
    headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36"
    headers["Referer"] = "http://jpg.mmjpg.com"
    img_content = requests.get(src,headers = headers).content
    #img_content = requests.get(src,).content
    with open(path,'wb') as f:
        f.write(img_content)


def getimg(base_url,url,path):
    #print(url)
    r = geturl(url)
    soup = BeautifulSoup(r.text,"lxml")

    #获取总页码
    temp = soup.find('div',{"class":"clearfloat"}).find("script").text
    total = int(re.findall("\d+",temp)[2])
    #print(soup.prettify())
    #print("total:"+str(total)+"!!!!!!!!")

    t = soup.find('div',id="content")
    #request.urlretrieve(t.find('img').get('src').strip(),path+'/'+'1.jpg')
    #print(t.find('img').get('src'))
    downjpg(t.find('img').get('src').strip(),path+'/1.jpg')

    if total<=1:
        return
    for i in range(2,total+1):
        url2 = url + '/' + str(i)
        r2 = geturl(url2)
        r2.encoding = 'utf-8'
        #f = open('./out.txt','w')
        #f.write(r2.text)
        #f.close()
        soup2 = BeautifulSoup(r2.text,"lxml")
        t2 = soup2.find('div',id="content")
        #print(t2.find('img').get('src'))
        #request.urlretrieve(t2.find('img').get('src').strip(),path+'/'+str(i)+'.jpg')
        #加判断，如果存在不下载图片，可续传
        img_path=path+'/'+str(i)+'.jpg'
        downjpg(t2.find('img').get('src').strip(),img_path)

    print(total+" imgs down!")

def getimglink(base_url,url,path,pool):
    headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36',
    "Host:": "192.168.1.1",
    "Connection":"keep-alive",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer":"http://www.mmjpg.com"
}

    r = geturl(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text,"lxml")

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
        #getimg(base_url,image_url,path+name)
        pool.apply_async(getimg,(base_url,image_url,path+name))
        x += 1
        #request.urlretrieve(image_url.strip(),'./pic/%s.jpg' % x)


if __name__ == '__main__':


    url = base_url = 'http://www.mmjpg.com/'
    #抓几页，每页10个
    page = 10
    path = './mmjpg/'

    #多进程
    process = 4
    pool = Pool(process)
    for page in range(1,page+1):
        if(page == 1):
            getimglink(base_url,url,path,pool)

            #pool.apply_async(getimglink,(base_url,url,path))
        else:
            url = base_url + '/home/' + str(page)

            getimglink(base_url,url,path,pool)

            #pool.apply_async(getimglink,(base_url,url,path))

    pool.close()
    pool.join()



