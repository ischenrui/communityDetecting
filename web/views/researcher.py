from flask import Flask, render_template, redirect, request ,Blueprint
import logging, json, os
import igraph as ig
import sys
sys.path.append("..")
from model.community_detect import cd_algorithm

researcher = Blueprint('researcher', __name__)

config = {}
config['ALLOWED_EXTENSIONS'] = set(['gml'])
config['UPLOAD_FOLDER'] = 'F:\\Temp\\gmldata\\temp'
config["ALGORITHM"] = set(["GN", "LPA", "CNM", "Louvain"])


@researcher.route('/researcher')
def echarts():
    return render_template('index_echarts.html')

@researcher.route("/upload_echarts", methods=["POST"])
def upload_echarts():
    file_info = request.files["file"]
    code = json.loads(request.form["code"])

    if file_info and allowed_file(file_info.filename):
        file_info.save(os.path.join(config['UPLOAD_FOLDER'], "temp.gml"))
    else:
        return  json.dumps({"error" : True, "msg" : "文件格式有误"})

    g = ig.Graph.Read_GML(os.path.join(config['UPLOAD_FOLDER'], "temp.gml"))

    back = {}
    for k in code:
        if k in config["ALGORITHM"]:
            jsondata = cd_algorithm.detecting(g, k)
            back[k] = format_data(jsondata)
        else:
            print("算法有误")

    return json.dumps(back)

def allowed_file(filename):
    """
    判断上传文件格式是否满足要求
    :param filename:
    :return:
    """
    global ALLOWED_EXTENSIONS
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config['ALLOWED_EXTENSIONS']


def format_data(data):
    """
    将算法返回的数据格式化为前端显示需要的数据格式
    :param data: 算法返回的数据集, 其中 community_data 的键是 class 的值，即为社区值
        {
            "nodes":[{"id": 1, "name": "张三","school": "", "insititution": "", "code": "0812", "teacherId": "", "class": 1, "centrality": 0.8889},...],
            "edges":[{"source": 2, "target": 1, "paper": 2, "patent": 8, "project": 1, "weight": 11},...],
            "community_data": [{"1": {"density": 0.6667, "transity": 0.6, "cluster": 0.5833}},...]
         }
    :return: 字典格式
        {
            "nodes":[{"name":1,"label":"张三","code":0812,"school":"","insititution":"","teacherId":"", "class": 0,"symbolSize": 10},,...],
            "links" : [{"source":1,"target":0,"paper":1,"patent":0,"project":0,"value":1 },...],
            "community_data": [{"1": {"density": 0.6667, "transity": 0.6, "cluster": 0.5833},...]
        }
    """
    data = json.loads(data)
    back_data = {
        "nodes" : [],
        "links" : [],
        "community" : data['community_data']
    }

    for node in data["nodes"]:
        node['label'], node['name'], node['category'] = node['name'], node['id'], node["class"]-1
        del node["id"], node["class"]
        back_data["nodes"].append(node)
    for link in data["edges"]:
        link["value"] = link["weight"]
        del link["weight"]
        back_data['links'].append(link)

    return back_data

