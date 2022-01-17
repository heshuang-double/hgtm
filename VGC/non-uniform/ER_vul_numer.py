import numpy as np
import networkx as nx
n=10000
m=3
r=0.08


def degree(z):
    node_degree = np.random.poisson(z,n)  # 超度序列
    edge_degree=[]
    sumnode_degree = 0
    for i in range(len(node_degree)):
        sumnode_degree += node_degree[i]

    sumedge_degree=0
    while sumedge_degree<sumnode_degree:
        edge = np.random.poisson(m)  # 超边规模
        edge_degree.append(edge)
        sumedge_degree=sumedge_degree+edge

    if sumedge_degree > sumnode_degree:
        node_degree[0]=node_degree[0]+(sumedge_degree-sumnode_degree)


    degree=[]
    degree.append(node_degree)
    degree.append(edge_degree)

    return degree


# 模拟脆弱巨分支的大小
def hyper(z):
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
                x_nei=0
                for u in G.neighbors(x):
                    x_nei=x_nei+(G.degree(u)-1)
                
                if x_nei!=0:
                    if (1/x_nei) >= r:
                        G.nodes[x]["act"] = 1
                
                else:
                    G.nodes[x]["act"] = 1
                    
            else:
                    G.nodes[x]["act"] = 1
                    
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
for z in np.arange(0.1,7.1,0.1):
    z_list.append(z)
    
    vulsum=0
    for t in range(100):   # 平均100次,每次随机
        vulsum=vulsum+hyper(z)
    vul.append(vulsum/100)


f=open('work\\non-uniform\\Sv_avg100\\ER_vul_numer3.txt','w+')  # 若磁盘中无此文件将自动新建
for i in range(len(z_list)):
    f.write(str(format(z_list[i], '.1f')))
    f.write(' ')
    f.write(str(format(float(vul[i]), '.4f')))
    f.write('\n')
f.close()

