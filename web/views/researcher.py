from flask import Flask, render_template, redirect, request ,Blueprint
import logging, json, os
import igraph as ig
import sys
sys.path.append("..")
from model.community_detect import cd_algorithm


researcher = Blueprint('researcher', __name__)

config = {}
config['ALLOWED_EXTENSIONS'] = set(['gml'])
config['UPLOAD_FOLDER'] = 'uploads'
config["ALGORITHM"] = set(["GN", "LPA", "CNM", "Louvain"])

@researcher.route('/researcher')
def echarts():
    return render_template('researcher_page.html')

@researcher.route("/upload_echarts", methods=["POST"])
def upload_echarts():
    file_info = request.files["file"]
    code = request.form["code"].split(",")
    if file_info and allowed_file(file_info.filename):
        file_info.save(os.path.join(config['UPLOAD_FOLDER'], "temp.gml"))
    else:
        return json.dumps({"error": True, "msg": "文件格式有误"})
    # g = ig.Graph.Read_GML(os.path.join(config['UPLOAD_FOLDER'], "temp.gml"))

    back = {}
    for k in code:
        if k in config["ALGORITHM"]:
            g = ig.Graph.Read_GML(os.path.join(config['UPLOAD_FOLDER'], "temp.gml"))
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
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config['ALLOWED_EXTENSIONS']


