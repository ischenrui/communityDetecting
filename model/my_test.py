from model.community_detect import cd_algorithm
import igraph as ig
import time
# school = '清华大学'
# insititution = '材料学院'
# code = ''
# path = 'F:\Temp\gmldata\source/%s%s%s'%(school,insititution,code)
# g = ig.Graph.Read_GML(path+'.gml')
#
# # 算法包括  Louvain,LPA,GN,CNM
# jsondata = cd_algorithm.detecting(g,'CNM')
#
# #
# # # JSON格式 {nodes:[{id,name,school,insititution,teacherId,class,centrality}],
# # #           edges:[{source,target,paper,project,patent,weight}],
# # #           community_data:{class:{density,transity,cluster}}}
# print(jsondata)
# f = open('F:\Temp\gmldata\json/%s%s%s.txt'%(school,insititution,code),'w',encoding='utf-8')
# f.write(jsondata)
# f.close()

# f = open('F:\Temp\gmldata\json/%s%s%s.txt'%(school,insititution,code),'r',encoding='utf-8')
# data = f.read()
# # print(data)
# import json
# xxx = json.loads(data)
# print(xxx)



# import csv
# data = csv.reader(
#         open('F:\myproject\python/biye\data/network/01_extract/nodes_neo4j_clean.csv', 'r', encoding='utf-8'))
# sndic = {'school': [], 'sch_ins': [], 'code': []}
# i = 0
# for node in data:
#     i += 1
#     if i != 1:
#         if node[2] not in sndic['school']: sndic['school'].append(node[2])
#         if node[2] + '-' + node[3] not in sndic['sch_ins']: sndic['sch_ins'].append(node[2] + '-' + node[3])
#         if node[4] not in sndic['code']: sndic['code'].append(node[4])
# for i in range(556,len(sndic['sch_ins'])):
# # for i in range(0,100):
#     print(i)
#     node = sndic['sch_ins'][i]
#     school = node.split('-')[0]
#     ins = node.split('-')[1]
#     try:
#         print(school,ins)
#         code = ''
#         path = 'F:\Temp\gmldata\source/%s%s%s'%(school,ins,code)
#         g = ig.Graph.Read_GML(path+'.gml')
#         jsondata = cd_algorithm.detecting(g, 'Louvain')
#         f = open('F:\\myproject\\python\\communityDetecting\\data\\%s%s%s.txt'%(school,ins,code),'w',encoding='utf-8')
#         f.write(jsondata)
#         f.close()
#     except:
#         print("没有---------------%s%s"%(school,ins))

    # print(school, ins)
    # code = ''
    # path = 'F:\Temp\gmldata\source/%s%s%s' % (school, ins, code)
    # g = ig.Graph.Read_GML(path + '.gml')
    # jsondata = cd_algorithm.detecting(g, 'Louvain')
    # f = open('F:\\myproject\\python\\communityDetecting\\data\\%s%s%s.txt' % (school, ins, code), 'w', encoding='utf-8')
    # f.write(jsondata)
    # f.close()

    # time.sleep(0.2)

f = open('E:\实习相关文件\实习文件\材料学院/teacher.txt','r',encoding='utf-8')
teacher = [_.strip() for _ in f.readlines()]
# print(teacher)

from  db.mydba import db_crpc

data = db_crpc.getDics('select NAME from eval_jiechu')
jiechu  = [_['NAME'].replace(' ','') for _ in data]

print(set(teacher)&set(jiechu))