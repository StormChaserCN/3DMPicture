import os
from multiprocessing.dummy import Pool as ThreadPool

import bs4
import requests

TARGET_PATH = 'D:/Media/Picture/3DM'
BASEURL = 'http://www.3dmgame.com/zt/201709/3686046.html'
PAGE_NUM = 44


def DownloadPic(url):
    pathinfo = url.split('/')
    dirinfo = BASEURL.split('/')
    dirname = TARGET_PATH + '/' + dirinfo[-1][:-5]
    try:
        r = requests.get(url)
        finfo = pathinfo[-1].split('.')
        if r.content[:3] == 'GIF':
            filepath = dirname + '/' + finfo[0] + '.gif'
        else:
            filepath = dirname + '/' + finfo[0] + '.jpg'
        with open(filepath, 'wb') as fd:
            fd.write(r.content)
        r.close()
    except:
        pass


def EnumPage(url):
    r = requests.get(url)
    if r.status_code != 200:
        return
    soup = bs4.BeautifulSoup(r.content, 'lxml')
    r.close()
    divs = soup.find('div', attrs={'class': 'page_fenye'})
    for imgs in divs.nextSibling.find_all('img'):
        imgpath = imgs.get('src')
        if imgpath[:4] == 'http':
            DownloadPic(imgpath)


if __name__ == '__main__':
    # download
    urlset = []
    urlset.append(BASEURL)
    for i in xrange(2, PAGE_NUM + 1):
        urlset.append(BASEURL[:-5] + '_' + str(i) + '.html')

    dirinfo = BASEURL.split('/')
    dirname = TARGET_PATH + '/' + dirinfo[-1][:-5]
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    pool = ThreadPool(processes=4)
    pool.map(EnumPage, urlset)
    pool.close()
    pool.join()

    print 'Done'
