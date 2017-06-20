# 专辑封面下载
### 运行环境
Python 2.7
### 爬取网站 'http://coverbox.sinaapp.com/'
### installing
```
pip install  -r requirements.txt
```
### Running
```
cd cover_box
scrapy crawl corver -a XXX  #注释 XXX 你需要下载的专辑名称，或歌手名字
```
### 图片保存地址
cover_box/picture/full
### Precautions
不要频繁的抓取，这个网站流量有上限
