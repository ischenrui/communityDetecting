from flask import Flask, render_template, redirect, request
import logging, json, os
import igraph as ig

import sys
sys.path.append("..")
from model.community_detect import cd_algorithm


app = Flask(__name__)

app.config['ALLOWED_EXTENSIONS'] = set(['gml'])
# app.config['UPLOAD_FOLDER'] = 'F:\\Temp\\gmldata\\temp'
app.config['UPLOAD_FOLDER'] = 'uploads'

app.config["ALGORITHM"] = set(["GN", "LPA", "CNM", "Louvain"])


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/upload", methods=["POST", "GET"])
def upload_file():
    file_info = request.files["file"]
    code = request.form["code"]
    print(code)

    data = {
        "nodes": [
            {"id": 0, "name": "孙晓丹", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 5,
             "label": "杰青"},
            {"id": 1, "name": "蔡强", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "杰青"},
            {"id": 2, "name": "李恒德", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "杰青"},
            {"id": 3, "name": "邵洋", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "杰青"},
            {"id": 4, "name": "陈娜", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "杰青"},
            {"id": 5, "name": "章晓中", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "杰青"}],

        "links": [
            {"source": 1, "target": 0, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 2, "target": 1, "paper": 0, "patent": 1, "project": 1, "weight": 2, "label": "同事"},
            {"source": 4, "target": 3, "paper": 0, "patent": 6, "project": 0, "weight": 6, "label": "同事"},
            {"source": 4, "target": 2, "paper": 0, "patent": 6, "project": 0, "weight": 6, "label": "同事"},
            {"source": 4, "target": 1, "paper": 0, "patent": 6, "project": 0, "weight": 6, "label": "同事"},
            {"source": 5, "target": 4, "paper": 0, "patent": 2, "project": 0, "weight": 2, "label": "同事"}
        ],

        "results": [
            {"title": "这是分析的标题", "msg": "这是第一条分析结果"},
            {"title": "标题可有可无", "msg": "这也是一条分析结果"},
            {"title": "", "msg": "这是一条没有标题的分析结果"}
        ]
    }

    return json.dumps(data)


@app.route('/echarts')
def echarts():
    return render_template('index_echarts.html')

@app.route("/upload_echarts", methods=["POST"])
def upload_echarts():
    file_info = request.files["file"]
    code = json.loads(request.form["code"])

    if file_info and allowed_file(file_info.filename):
        file_info.save(os.path.join(app.config['UPLOAD_FOLDER'], "temp.gml"))
    else:
        return  json.dumps({"error" : True, "msg" : "文件格式有误"})

    g = ig.Graph.Read_GML(os.path.join(app.config['UPLOAD_FOLDER'], "temp.gml"))

    back = {}
    for k in code:
        if k in app.config["ALGORITHM"]:
            # jsondata = cd_algorithm.detecting(g, k)
            # back[k] = format_data(jsondata)
            back[k] = cd_algorithm.detecting(g, k)
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
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(host="127.0.0.1",debug=True)
