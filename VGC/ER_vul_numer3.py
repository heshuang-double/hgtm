import numpy as np
import networkx as nx
n=10000
m=3
r=0.08

'''
配置模型是将两边伸出的线头均匀随机地连完，
如果在连边过程中考虑避免自边和重边的话，那就不是均匀随机了，
Newman那本书里面也讲了，配置模型的生成过程必然导致自边和重边的无法避免。

Bollobás (1980)指出，很有可能产生平行边（相当于自边），即一个节点有多个线头属于同一条超边，
但平行边相对网络规模而言很小，可以在生成完网络之后删去。

那会不会有这样的情况：超边1包含a和b，超边2包含a和b，这样不就算重边了嘛？
不过文献没讲这个，暂不考虑，这样的可能性也比较小。

下面生成二分图（超图可以认为是二分图）的程序和之前图的一样，利用自带的库来实现。
'''


def degree(z):
    node_degree = np.random.poisson(z,n)  # 超度序列
    sumnode_degree = 0
    for i in range(len(node_degree)):
        sumnode_degree += node_degree[i]

    while (sumnode_degree % m != 0):
        node_degree[0] += 1   # 超度序列
        sumnode_degree += 1
    
    edgenum=int(sumnode_degree/m)

    edge_degree=[]
    for i in range(edgenum):
        edge_degree.append(m)  # 超边规模序列

    degree=[]
    degree.append(node_degree)
    degree.append(edge_degree)

    return degree


'''
算这个网络的脆弱巨分支，相变点，崩溃窗口，激活态节点的比例，
先考虑每个节点阈值都一样的情形
    
相变公式和脆弱巨分支的理论值依赖于理论推导
下面先考虑脆弱巨分支的模拟值，模拟激活态节点的比例
'''


# 模拟脆弱巨分支的大小
def hypernetwork(z):
    degree_seq=degree(z)
    node_seq=degree_seq[0]
    edge_seq=degree_seq[1]


    G=nx.algorithms.bipartite.generators.configuration_model(node_seq, edge_seq)
    
    # 算法实际执行过程中把超边也当成了节点
    
    for x in range(len(node_seq)): 
        G.add_node(x,act=0)

    for x in range(len(node_seq)): # 判断脆弱点
        if G.nodes[x]["act"]==0:
            if G.degree(x)!=0:
                
                '''
                若有节点和x同属于多条超边，也要多算几次，
                因为综述里面是说邻接矩阵的元素值为同时包含两个节点的超边数量，并非一定是1
                '''

                if (1/(G.degree(x)*(m-1))) >= r:
                    G.nodes[x]["act"] = 1

            else:
                G.nodes[x]["act"] = 1  # 孤立节点直接定义为脆弱点

    for x in range(len(node_seq)):  # 删掉那些非脆弱的节点
        if G.nodes[x]["act"]==0:
            inact=set()
            for y in G.neighbors(x):   # 非脆弱节点x所属的那些超边
                inact.add(y)
            
            if len(inact) != 0:
                for y in inact:
                    G.remove_edge(x,y)   # 非脆弱节点x不在超边y当中了

    # 求分支规模 BFS
    i = 0
    componentlen = np.zeros(shape=n, dtype=int)
    node_seen = set()
    for s in range(len(node_seq)):
        if s not in node_seen:
            queue = []
            queue.append(s)       # 向list添加元素，用append()
            node_seen.add(s)   # 向set添加函数，用add()
            while (len(queue) > 0):
                vertex = queue.pop(0)  # 提取队头
                componentlen[i] = componentlen[i] + 1
                edges = G[vertex]  # 获得队头元素的邻接元素

                for e in edges:
                    for w in G.neighbors(e):
                        if w not in node_seen:
                            queue.append(w)  # 将没有遍历过的子节点入队
                            node_seen.add(w)    # 标记好已遍历
        i = i + 1
    
    return(max(componentlen)/n)


z_list=[]
vul=[]
for z in np.arange(0.1,10.1,0.1):
    z_list.append(z)
    
    vulsum=0
    for t in range(100):   # 平均100次,每次的网络随机
        vulsum=vulsum+hypernetwork(z)
    vul.append(vulsum/100)


f=open('work\\uniform\\poisson\\Sv_avg100\\ER_vul_numer3.txt','w+')  # 若磁盘中无此文件将自动新建
for i in range(len(z_list)):
    f.write(str(format(z_list[i], '.1f')))
    f.write(' ')
    f.write(str(format(float(vul[i]), '.4f')))
    f.write('\n')
f.close()

