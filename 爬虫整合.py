import requests,sys
from bs4 import BeautifulSoup


class downloader(object):

    
    def __init__(self):
        self.server='http://www.biqugex.com'
        self.target='http://www.biqugex.com/book_38927/'
        self.names=[]       #存放章节名
        self.urls=[]        #存放章节链接
        self.nums=0         #章节数


    '''
    函数说明：获取下载链接
    '''
    def get_download_url(self):
        req=requests.get(url=self.target)
        html=req.text
        
        div_bs=BeautifulSoup(html,'html.parser')
        div=div_bs.find_all('div',class_='listmain')
        
        a_bs=BeautifulSoup(str(div[0]),'html.parser')
        a=a_bs.find_all('a')

        self.nums=len(a[21:])       #剔除不必要的章节，并统计章节数
        for each in a[21:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))


    '''
    函数说明：获取章节内容
    '''
    def get_contents(self,target):
        req=requests.get(url=target)
        html=req.text
        bs=BeautifulSoup(html,'html.parser')      #得到一个 BeautifulSoup 的对象
        texts=bs.find_all('div',class_='showtxt')
        texts=texts[0].text.replace('\xa0' *8, '\n\n')      #将八个 &nbsp;（空格） 替换为换行
        texts=texts.replace('　　'+target+'　　天才一秒记住本站地址：www.biqugex.com。笔趣阁手机版阅读网址：m.biqugex.com','')
        return texts


    '''
    函数说明：将爬取的文章内容写入文件
    '''
    def writer(self,name,path,text):
        write_flag=True
        with open(path,'a',encoding='utf-8') as f:
            f.write(name+'\n')
            f.writelines(text)
            f.write('\n\n')

            
if __name__=='__main__':
    dl=downloader()
    dl.get_download_url()
    print('《地府朋友圈》开始下载：')
    for i in range(dl.nums):
        dl.writer(dl.names[i],'地府朋友圈.txt',dl.get_contents(dl.urls[i]))
        #sys.stdout.write("  已下载：%.3f%%"%float(i/dl.nums)+'\r')
        sys.stdout.write("  已下载：%.3f%%"%float((i/dl.nums)*100)+'\r')
        sys.stdout.flush()
    print('《地府朋友圈》下载完成')
