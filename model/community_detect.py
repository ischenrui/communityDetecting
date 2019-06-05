import networkx as nx
import json
import time

def get_json(g,community_data):
    data = {'nodes': [], 'edges': [] }
    data['community_data'] = community_data
    for node in g.vs:
        tnode = {}
        tnode['id'] = int(node['id'])
        tnode['name'] = node['name']
        tnode['code'] = node['code']
        tnode['school'] = node['school']
        tnode['insititution'] = node['insititution']
        tnode['teacherId'] = node['teacherId']
        tnode['class'] = node['class']
        tnode['centrality'] = node['centrality']
        data['nodes'].append(tnode)
    elist = g.get_edgelist()
    for i in range(0, len(g.es)):
        tedge = {}
        tedge['source'] = elist[i][1]
        tedge['target'] = elist[i][0]
        tedge['paper'] = int(g.es[i]['paper'])
        tedge['patent'] = int(g.es[i]['patent'])
        tedge['project'] = int(g.es[i]['project'])
        tedge['weight'] = int(g.es[i]['weight'])
        data['edges'].append(tedge)
    return json.dumps(data)

def getColor(value):
    colorList = ['blue','green','purple','yellow','red','pink','orange','black','white','gray','brown','wheat']
    return colorList[int(value)]

def add_label(c,g):
    tlist = [0] * len(g.vs)
    for i in range(0, len(c)):
        for node in c[i]:
            tlist[node] = i + 1
    g.vs['class'] = tlist
    return g

def density(g):
    #密度
    a = len(g.edges())
    n = len(g.nodes())
    return a/(n*(n-1)/2)

def cluster_coefficient(g):
    #聚集系数
    a = nx.clustering(g)
    sum = 0
    for k,v in a.items():
        sum+=v
    return sum/len(g.nodes())

def get_community_data(g):
    # 获取社区分析数据，包括 密度，传递系数，聚集系数
    t_dic = {}
    for i in range(0,len(g.vs['class'])):
        label = g.vs['class'][i]
        if label in t_dic.keys():t_dic[label].append(i)
        else:t_dic[label] = [i]
    out = {}
    for k,v in t_dic.items():
        if len(v)>2:
            out[k] = {}
            subg = g.subgraph(v).copy()
            edgelist = subg.get_edgelist()
            nxg = nx.Graph(edgelist)
            out[k]['density'] = round(density(nxg),4) #密度
            out[k]['transity'] = round(nx.transitivity(nxg),4)  #传递性
            out[k]['cluster'] = round(cluster_coefficient(nxg),4) #聚集系数
        else:out[k] = {'density':0,'transity':0,'cluster':0}
    return out

def add_centrality(g):
    t_dic = {}
    for i in range(0, len(g.vs['class'])):
        label = g.vs['class'][i]
        if label in t_dic.keys():
            t_dic[label].append(i)
        else:
            t_dic[label] = [i]

    n = len(t_dic)
    my_dic = {} #记录节点分析数据
    for k, v in t_dic.items():
        if len(v) > 2:
            subg = g.subgraph(v)
            edgelist = subg.get_edgelist()
            nxg = nx.Graph(edgelist)
            a = nx.degree_centrality(nxg)   #节点度中心系数
            b = nx.closeness_centrality(nxg)    #节点距离中心系数
            c = nx.betweenness_centrality(nxg)  #节点介数中心系数
            subg_n = len(subg.vs)
            result = [(a[i] + b[i] + c[i]) / 3 for i in range(0,subg_n)]
            for i in range(0,subg_n):
                tid = subg.vs['teacherId'][i]
                my_dic[tid] = round(result[i],4)
        else:
            n -= 1
    score_list = []
    for node in g.vs:
        tid = node['teacherId']
        if tid in my_dic.keys():score_list.append(my_dic[tid])
        else:score_list.append(0)
    g.vs['centrality'] = score_list

    return g


class cdutil:
    def __init__(self):
        pass

    def detecting(self,g, type='Louvain'):
        print('社区发现算法%s开始...' % type)
        t1 = time.time()
        weights = g.es['weight']
        if type == 'LPA':
            c = list(g.community_label_propagation(weights=weights).as_cover())
        elif type == 'GN':
            c = list(g.community_edge_betweenness(weights=weights).as_clustering())
        elif type == 'CNM':
            c = list(g.community_fastgreedy(weights=weights).as_clustering())
        elif type == 'Louvain':
            c = list(g.community_multilevel(weights=weights).as_cover())
        g = add_label(c, g)
        print('社区发现算法%s运行完毕,耗时%s...' % (type, time.time() - t1))
        print('社区分析%s开始...' % type)
        t1 = time.time()
        g = add_centrality(g)
        community_data = get_community_data(g)
        print('社区分析%s运行完毕,耗时%s...' % (type, time.time() - t1))
        return get_json(g, community_data)

cd_algorithm = cdutil()