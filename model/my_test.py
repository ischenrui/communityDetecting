from model.community_detect import cd_algorithm
import igraph as ig
import json

school = '清华大学'
insititution = '材料学院'
code = ''
path = 'E:/code/communityDetecting/web/uploads/temp'
g = ig.Graph.Read_GML(path+'.gml')

# 算法包括  Louvain,LPA,GN,CNM
jsondata = cd_algorithm.detecting(g,'CNM')


# JSON格式 {nodes:[{id,name,school,insititution,teacherId,class,centrality}],
#           edges:[{source,target,paper,project,patent,weight}],
#           community_data:{class:{density,transity,cluster}}}
print(jsondata)

with open("back.json", "wb") as f:
    # f.write(json.dumps(jsondata).encode("gbk"))
    f.write(jsondata.encode("gbk"))