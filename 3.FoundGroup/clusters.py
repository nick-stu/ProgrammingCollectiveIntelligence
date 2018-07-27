# 从文件读取数据
def readfile(filename):
    lines=[line for line in open(filename)]

    # 第一行是列标题
    colnames=lines[0].strip().split('\t')[1:]
    rowname=[]
    data=[]
    for line in lines[1:]:
        p=line.strip().split('\t')
        # 每一行的第一列是行名
        rowname.append(p[0])
        # 剩余部分就是该行的数据
        data.append([float(x) for x in p[1:]])
    return rowname,colnames,data

from math import sqrt
def pearson(v1, v2):
    # Simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

    # Sums of the squares
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    # Sum of the products
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))
    if den == 0: return 0
    # 使相似度越大的两个元素之间的距离越小
    return 1.0 - num / den

# 聚类类型
class bicluster:
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left=left
        self.right=right
        self.vec=vec
        self.id=id
        self.distance=distance

# 层次聚类
def hcluster(rows,distance=pearson):
    distances={}
    currentclustid=-1

    # 最开始的聚类就是数据集中的行
    clust=[bicluster(rows[i],id=i) for i in range(len(rows))]

    while len(clust)>1:
        lowestpair=(0,1)
        closest=distance(clust[0].vec,clust[1].vec)

        # 遍历每一个配对，寻找最小距离
        for i in range(len(clust)):
            for j in range(i+1,len(clust)):
                # 用distances来缓存距离的计算值
                if (clust[i].id,clust[j].id) not in distances:
                    distances[(clust[i].id,clust[j].id)]=distance(clust[0].vec,clust[1].vec)
                d=distances[(clust[i].id,clust[j].id)]

                if d<closest:
                    closest=d
                    lowestpair=(i,j)

        # 计算两个聚类的平均值
        mergevec = [
            (clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0
            for i in range(len(clust[0].vec))]

        # create the new cluster
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]],
                               right=clust[lowestpair[1]],
                               distance=closest, id=currentclustid)

        # cluster ids that weren't in the original set are negative
        currentclustid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]

def printclust(clust,labels=None,n=0):
    # 利用缩进来建立层次布局
    for i in range(n): print(' ',end = '')
    if clust.id<0:
        # 负数代表这是一个分支
        print('-')
    else:
        # 正数标记这是叶节点
        if labels==None: print(clust.id)
        else: print(labels[clust.id])

    # 现在打印右侧分支和左侧分支
    if clust.left!=None: printclust(clust.left,labels=labels,n=n+1)
    if clust.right!=None: printclust(clust.right,labels=labels,n=n+1)

from PIL import Image,ImageDraw
def getheight(clust):
    if clust.left==None and clust.right==None: return 1
    return getheight(clust.left)+getheight(clust.right)

def getdepth(clust):
    # 一个叶节点的距离是0.0
    if clust.left==None and clust.right==None: return 0
    # 一个枝节点的距离等于左右分支中距离较大者加上其本身的距离
    return max(getdepth(clust.left),getdepth(clust.right))+clust.distance

def drawdendrogram(clust,labels,jpeg='clusters.jpg'):
    # 高度和宽度
    h=getheight(clust)*20
    w=1200
    depth=getdepth(clust)
    # width is fixed, so scale distances accordingly
    scaling=float(w-150)/depth

    # 新建白色背景的图片
    img=Image.new('RGB',(w,h),(255,255,255))
    draw=ImageDraw.Draw(img)

    draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))

    # Draw the first node
    drawnode(draw, clust, 10, (h / 2), scaling, labels)
    img.save(jpeg, 'JPEG')

def drawnode(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        h1 = getheight(clust.left) * 20
        h2 = getheight(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2
        # Line length
        ll = clust.distance * scaling
        # Vertical line from this cluster to children
        draw.line((x, top + h1 / 2, x, bottom - h2 / 2), fill=(255, 0, 0))

        # Horizontal line to left item
        draw.line((x, top + h1 / 2, x + ll, top + h1 / 2), fill=(255, 0, 0))

        # Horizontal line to right item
        draw.line((x, bottom - h2 / 2, x + ll, bottom - h2 / 2), fill=(255, 0, 0))

        # Call the function to draw the left and right nodes
        drawnode(draw, clust.left, x + ll, top + h1 / 2, scaling, labels)
        drawnode(draw, clust.right, x + ll, bottom - h2 / 2, scaling, labels)
    else:
        # If this is an endpoint, draw the item label
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))
# 水平线长度代表差别，而垂直线长度只是为了构图规整

# 可进行列聚类
def rotatematrix(data):
    newdata=[]
    for i in range(len(data[0])):
        newrow=[data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata

##################################### kmeans #########################################
import random
def kluster(rows,distance=pearson,k=4):
    # 确定每一维的最小值和最大值
    ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows]))
            for i in range(len(rows[0]))]
    # Create k randomly placed centroids
    clusters = [ [random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0]
                 for i in range(len(rows[0]))] for j in range(k)]
    lastmatches=None
    for t in range(100):
        print('Iteration %d' % t)
        # 类集合标签
        bestmatches=[[] for i in range(k)]

        # 在每一行中寻找距离最近的中心点
        for j in range(len(rows)):
            row=rows[j]
            bestmatch=0
            # 依次比对k个中心点，最近的中心点则为bestmatch
            for i in range(k):
                d=distance(clusters[i],row)
                if d<distance(clusters[bestmatch],row): bestmatch=i
            # 将该样本点加入该中心点类中
            bestmatches[bestmatch].append(j)

        # 如果结果和上次相同，则退出
        if bestmatches==lastmatches: break
        lastmatches=bestmatches

        # 更新中心点
        for i in range(k):
            avgs=[0.0]*len(rows[0])
            if len(bestmatches[i])>0:
                # 累加
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m]+=rows[rowid][m]
                # 平均
                for j in range(len(avgs)):
                    avgs[j]/=len(bestmatches[i])
                clusters[i]=avgs
    return bestmatches


def tanimoto(v1,v2):
    c1,c2,shr=0,0,0

    for i in range(len(v1)):
        if v1[i]!=0: c1+=1
        if v2[i]!=0: c2+=1
        if v1[i]!=0 and v2[i]!=0: shr+=1
    return 1.0-(float(shr)/(c1+c2-shr))

def scaledown(data,distance=pearson,rate=0.01):
    n=len(data)