import networkx as nx
import json
import time
import igraph as ig

def get_json(g, cover,core_node,q_,c_,s_,community_data):
    """
        转化为json结果
        :return: json格式
            {
            "nodes":[{"id": 0, "name": "张三", "code": "0805", "school": "清华大学", "insititution": "材料学院", "teacherId": "135391", "class": 1},...],
            "edges": [{"source": 1, "target": 0, "paper": 0, "patent": 0, "project": 1, "weight": 1},...]
            "community_data": [{"1": {"density": 0.6, "transity": 0.5455, "scale": 5},...}
            "algorithm_compare": [{"cover": 0.9178082191780822, "Q": 0.6667031923442183, "C": 0.5580385487528344, "S": 0.75}]
            "core_node": [0,3,...]
            }
            说明：
            {
            "nodes"中，"class"是社区编号
            "community_data": 中"scale"是社区规模，即社区内节点个数
            "algorithm_compare": 中"cover"是节点覆盖率, "Q"是模块度, "C"是聚集系数, "S"是社区强度
            "core_node": 是各个社区中综合中心度最高的节点
            }
        """
    data = {'nodes': [], 'edges': []}
    class_list = list(set(g.vs['class']))
    tid_list = [int(_)for _ in g.vs['teacherId']]
    for node in g.vs:
        tnode = {}
        tnode['teacherId'] = int(node['teacherId'])
        # tnode['id'] = int(node['id'])
        tnode['name'] = node['name']
        tnode['code'] = node['code']
        tnode['school'] = node['school']
        tnode['insititution'] = node['insititution']
        tnode['class'] = class_list.index(node['class'])+1
        tnode['centrality'] = node['centrality']
        data['nodes'].append(tnode)

    elist = g.get_edgelist()
    for i in range(0, len(g.es)):
        tedge = {}
        tedge['source'] = tid_list[elist[i][1]]
        tedge['target'] = tid_list[elist[i][0]]
        tedge['paper'] = int(g.es[i]['paper'])
        tedge['patent'] = int(g.es[i]['patent'])
        tedge['project'] = int(g.es[i]['project'])
        tedge['weight'] = int(g.es[i]['weight'])
        data['edges'].append(tedge)
    data['community_data'] = list(community_data)
    data['algorithm_compare'] = [{"cover": cover, "Q": q_, "C": c_, "S": s_}]
    id_list = g.vs['id']
    data['core_node'] = [tid_list[id_list.index(_)] for _ in core_node]
    return json.dumps(data)

def getColor(value):
    colorList = ['blue','green','purple','yellow','red','pink','orange','black','white','gray','brown','wheat']
    return colorList[int(value)]

def get_cover(g,c):
    d = []
    for vs in c:
        if len(vs) < 3:
            d.extend(vs)
    return 1-len(d)/len(g.vs)

def add_label(c,g):
    # 添加社区标签，并且删除社区规模小于3的节点
    tlist = [0] * len(g.vs)
    for i in range(0, len(c)):
        for node in c[i]:
            tlist[node] = i + 1
    g.vs['class'] = tlist
    d = []
    for vs in c:
        if len(vs)<3:
            d.extend(vs)
    g.delete_vertices(d)

    g.vs['id'][0] = 1000

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
    # 获取社区分析数据，包括 密度，传递系数，社区规模
    t_dic = {}
    for i in range(0,len(g.vs['class'])):
        label = g.vs['class'][i]
        if label in t_dic.keys():t_dic[label].append(i)
        else:t_dic[label] = [i]
    out, back = {}, []
    for k,v in t_dic.items():
        if len(v)>2:
            out[k] = {}
            subg = g.subgraph(v).copy()
            edgelist = subg.get_edgelist()
            nxg = nx.Graph(edgelist)
            out[k]['density'] = round(density(nxg),4) #密度
            out[k]['transity'] = round(nx.transitivity(nxg),4)  #传递性
            out[k]['scale'] = len(v)
        else:out[k] = {'density':0,'transity':0,'scale':0}
        back.append({k:out[k]})
    return back

def get_Q(g):
    # 计算划分后社区的模块度值
    return g.modularity(g.vs['class'])

def get_C(g):
    # 计算划分后社区的聚集系数
    t_dic = {}
    for i in range(0, len(g.vs['class'])):
        label = g.vs['class'][i]
        if label in t_dic.keys():
            t_dic[label].append(i)
        else:
            t_dic[label] = [i]

    n = len(t_dic)
    c = 0
    for k, v in t_dic.items():
        if len(v) > 2:
            subg = g.subgraph(v).copy()
            edgelist = subg.get_edgelist()
            nxg = nx.Graph(edgelist)
            c += cluster_coefficient(nxg)  #
        else:
            n -= 1
    return c / n

def get_S(g):
    # 计算划分后社区的强度
    t_dic = {}
    for i in range(0, len(g.vs['class'])):
        label = g.vs['class'][i]
        if label in t_dic.keys():
            t_dic[label].append(i)
        else:
            t_dic[label] = [i]
    n = len(t_dic)
    neb = g.neighborhood()
    s = 0
    for k, v in t_dic.items():
        if len(v) > 2:
            flag = 0
            iner_sum = 0
            outer_sum = 0
            for node in v:
                node_all_neb = neb[node][1:]
                outer = len(set(node_all_neb)-set(v))
                iner = len(node_all_neb) - outer
                iner_sum+=iner
                outer_sum+=outer
                if iner<outer:flag = 1
            if flag==0:s+=1
            elif iner_sum>outer_sum:s+=0.5
            # else:print('无')
        else:
            n -= 1
    return s/n


def get_QCS(g):
    q = get_Q(g)
    c = get_C(g)
    s = get_S(g)

    return q,c,s


def get_core_node(g):
    """
    得到每个社区的核心节点
    :return: 列表元素 {社区编号：核心节点ID}
        [{1: 0}, {2: 3}, ..., {18: 77}]
    """
    t_dic = {}
    for i in range(0, len(g.vs['class'])):
        # id = g.vs['id'][i]
        label = g.vs['class'][i]
        if label in t_dic.keys():
            t_dic[label].append(i)
        else:
            t_dic[label] = [i]

    out = []
    my_dic = {}  # 记录节点分析数据
    for k, v in t_dic.items():
        subg = g.subgraph(v).copy()
        edgelist = subg.get_edgelist()
        nxg = nx.Graph(edgelist)
        a = nx.degree_centrality(nxg)  # 节点度中心系数
        b = nx.closeness_centrality(nxg)  # 节点距离中心系数
        c = nx.betweenness_centrality(nxg)  # 节点介数中心系数
        subg_n = len(subg.vs)
        result = [(a[i] + b[i] + c[i]) / 3 for i in range(0, subg_n)]
        i = result.index(max(result))
        a = subg.vs['id'][i]
        out.append(int(a))

        for i in range(0, subg_n):
            tid = subg.vs['teacherId'][i]
            my_dic[tid] = round(result[i], 4)

    score_list = []
    for node in g.vs:
        tid = node['teacherId']
        if tid in my_dic.keys():
            score_list.append(my_dic[tid])
        else:
            score_list.append(0)
    g.vs['centrality'] = score_list
    return out,g

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
        cover = get_cover(g, c)
        core_node,g = get_core_node(g)
        q_,c_,s_ = get_QCS(g)
        community_data = get_community_data(g)


        return get_json(g, cover,core_node,q_,c_,s_,community_data)

cd_algorithm = cdutil()