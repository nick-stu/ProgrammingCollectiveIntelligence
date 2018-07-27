import urllib.request
import time

opener = urllib.request.build_opener()
opener.addheaders=[('User-agent','Mozilla/5.0')]
file=open('feedlist.txt')
lines = file.readlines()
aa = []
for line in lines:
    temp=line.replace('\n','')
    aa.append(temp)

print('Begin.......')
out=open('feedlist_accessible.txt','w')
for a in aa:
    tempUrl = a
    try:
        opener.open(tempUrl)
        print(tempUrl+' OK')
        out.write(tempUrl+'\n')
    except:
        print(tempUrl+' ERROR')