#coding:utf-8

#实现了保存一个url中所有图片的功能
import requests
from bs4 import BeautifulSoup
from urllib import request

#保存一个url中所有图片
def getimg(url):
    r = requests.get(url)
    #解决乱码
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text)

    for img in soup.find_all('img'):
        #print(img.get('src'))
        image_url = img.get('src')
        name = img.get('alt')
        request.urlretrieve(image_url.strip(),'./pic/'+name+'.jpg')
        #request.urlretrieve(image_url.strip(),'./pic/%s.jpg' % x)


if __name__ == '__main__':


    url = 'http://www.99mm.me'
    #抓几页，每页10个
    page = 1
    for p in range(1,page+1):
        if(page == 1):
            getimg(url)
        else:
            url2 = url + '/hot/mm_4_'+str(page)+'.html'
            getimg(url2)

