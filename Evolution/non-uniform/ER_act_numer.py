import numpy as np
import networkx as nx
n=10000
m=3
r=0.08
z=3
tmax=30


def degree():
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
 

# 模拟激活态节点比例
def hyper():
    degree_seq=degree()
    node_seq=degree_seq[0]
    edge_seq=degree_seq[1]

    G=nx.algorithms.bipartite.generators.configuration_model(node_seq, edge_seq)
    
    sumact_t=np.zeros(shape=tmax+1, dtype=float)
    avgact_t=np.zeros(shape=tmax+1, dtype=float)

    for u in range(20):
        for x in range(len(node_seq)): 
            G.add_node(x,act=0)

        seed=[]
        seedsize=1  # 初始种子数目

        while len(seed)<seedsize:
            se=np.random.randint(n)
            if G.degree(se) != 0:
                seed.append(se)
                G.nodes[se]["act"] = 1
    
        act_t=[]  # 激活态节点数目;每一时刻去检查每个节点是否会被激活
        act_t.append(len(seed))
        node_seen=0
        t=0

        act_pre=[]
    
        for x in seed: #判断种子的邻居是否被激活
            node_seen=node_seen+1
            for e in G.neighbors(x):  # x所属的超边e
                for y in G.neighbors(e):   # 考虑y是否能被激活
                    if G.nodes[y]["act"]==0:
                        an=0
                        for u in G.neighbors(y):
                            for v in G.neighbors(u):
                                if G.nodes[v]["act"]==1:
                                    an=an+1
                        
                        y_nei=0
                        for u in G.neighbors(y):
                            y_nei=y_nei+(G.degree(u)-1)


                        if (an/y_nei)>=r:
                            G.nodes[y]["act"]=1
                            seed.append(y)
            if t>=1:
                if node_seen==act_t[t]-act_t[t-1]:
                    act_t.append(len(seed))
                    t=t+1
                    node_seen=0
            else:
                if node_seen==act_t[t]:
                    act_t.append(len(seed))
                    t=t+1
                    node_seen=0
        
        for t in range(len(act_t)):
            act_pre.append(act_t[t])

        for t in range(len(act_t),tmax+1):
            act_pre.append(act_t[len(act_t)-1])

        for t in range(tmax+1):
            sumact_t[t]=sumact_t[t]+act_pre[t]

        for t in range(tmax+1):
            avgact_t[t]=sumact_t[t]/20


    return (avgact_t)  # 激活态节点数目


sumact_fraction=np.zeros(shape=tmax+1, dtype=float)
t_list=[]
for t in range(tmax+1):
    t_list.append(t)

for j in range(20):
    act_t=hyper()

    for i in range(tmax+1):
        sumact_fraction[i]=sumact_fraction[i]+act_t[i]/n


f=open('work\\non-uniform\\poisson_k\\act_fraction_avg2020\\poisson3\\ER_act_numer3.txt','w+')  # 若磁盘中无此文件将自动新建
for i in range(len(t_list)):
    f.write(str(format(t_list[i])))
    f.write(' ')
    f.write(str(format(float(sumact_fraction[i]/20), '.4f')))
    f.write('\n')
f.close()
