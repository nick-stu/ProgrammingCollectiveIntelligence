import feedparser
import re
from xlwt import *

# 返回一个RSS订阅源的标题和包含单词计数情况的字典
def getwordcounts(url):
    # 解析订阅源
    d = feedparser.parse(url)
    wc = {}
    # 循环遍历所有文章条目
    for e in d.entries:
        if 'summary' in e: summary=e.summary
        else: summary=e.description

        # 提取一个单词列表
        words=getwords(e.title+' '+summary)
        for word in words:
            wc.setdefault(word,0)
            wc[word]+=1
    return d.feed.title,wc

def getwords(html):
    # 去除所有html标记
    txt = re.compile(r'<[^>]+>').sub('',html)

    # 利用所有非字母字符拆分出单词
    words=re.compile(r'[^A-Z^a-z]+').split(txt)

    # 转化成小写形式
    return [word.lower() for word in words if word!='']

# 生成数据集
apcount={} # 出现这些单词的博客数目
wordcounts={} # 不同博客中不同单词的数目
feedlist=[line for line in open('feedlist_accessible.txt')]
c = 0
for feedurl in feedlist:
    c+=1
    print(c)
    title,wc=getwordcounts(feedurl)
    wordcounts[title]=wc
    for word,count in wc.items():
        apcount.setdefault(word,0)
        if count>1:
            apcount[word]+=1

# 得出有价值的单词列表
wordlist=[]
for w,bc in apcount.items():
    frac=float(bc)/len(feedlist)
    if frac>0.1 and frac<0.5: wordlist.append(w)

# 存储结果文件
# txt
# out=open('blogdata.txt','w')
# out.write('Blog')
# for word in wordlist: out.write('\t%s' % word)
# out.write('\n')
# for blog,wc in wordcounts.items():
#     out.write(blog)
#     for word in wordlist:
#         if word in wc: out.write('\t%d' % wc[word])
#         else: out.write('\t0')
#     out.write('\n')
# excel
file = Workbook(encoding = 'utf-8')
table = file.add_sheet('blogdata')
table.write(0,0,'Blog')
i=0
j=0
for word in wordlist:
    i+=1
    table.write(i,0,word)
for blog,wc in wordcounts.items():
    j+=1
    i=0
    table.write(0,j,blog)
    for word in wordlist:
        i+=1
        if word in wc: table.write(i,j,wc[word])
        else: table.write(i,j,0)

file.save('blogdata.xls')