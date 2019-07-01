from model.community_detect import cd_algorithm
import igraph as ig

school = '清华大学'
insititution = '材料学院'
code = ''
path = 'F:\Temp\gmldata\source/%s%s%s'%(school,insititution,code)
g = ig.Graph.Read_GML(path+'.gml')
jsondata = cd_algorithm.detecting(g)
print(jsondata)