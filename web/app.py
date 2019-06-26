from flask import Flask, render_template, redirect, request
import logging, json, os

from model.community_detect import cd_algorithm
import igraph as ig

app = Flask(__name__)

app.config['ALLOWED_EXTENSIONS'] = set(['gml'])
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
             "label": "杰青"},
            {"id": 6, "name": "姚可夫", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "杰青"},
            {"id": 7, "name": "张华伟", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "杰青"},
            {"id": 8, "name": "陈祥", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "杰青"},
            {"id": 9, "name": "刘源", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "杰青"},
            {"id": 10, "name": "李言祥", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "杰青"},
            {"id": 11, "name": "郭志鹏", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 0,
             "label": "杰青"},
            {"id": 12, "name": "董洪标", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 0,
             "label": "杰青"},
            {"id": 13, "name": "黄正宏", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 0,
             "label": "杰青"},
            {"id": 14, "name": "盖国胜", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 0,
             "label": "长江学者"},
            {"id": 15, "name": "齐龙浩", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 0,
             "label": "长江学者"},
            {"id": 16, "name": "康飞宇", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 0,
             "label": "长江学者"},
            {"id": 17, "name": "万春磊", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 0,
             "label": "长江学者"},
            {"id": 18, "name": "龚江宏", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 0,
             "label": "长江学者"},
            {"id": 19, "name": "谢志鹏", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 0,
             "label": "长江学者"},
            {"id": 20, "name": "张政军", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 0,
             "label": "杰青"},
            {"id": 21, "name": "潘伟", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 0,
             "label": "杰青"},
            {"id": 22, "name": "康进武", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 0,
             "label": "杰青"},
            {"id": 23, "name": "巩前明", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 0,
             "label": ""},
            {"id": 24, "name": "韩志强", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 0,
             "label": ""},
            {"id": 25, "name": "熊守美", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": ""},
            {"id": 26, "name": "柳百成", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": ""},
            {"id": 27, "name": "沈厚发", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "杰青"},
            {"id": 28, "name": "吕瑞涛", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "杰青"},
            {"id": 29, "name": "荆涛", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 3,
             "label": "杰青"},
            {"id": 30, "name": "刘剑波", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 3,
             "label": "杰青"},
            {"id": 31, "name": "赖文生", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 3,
             "label": "杰青"},
            {"id": 32, "name": "柳百新", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 3,
             "label": "杰青"},
            {"id": 33, "name": "沈洋", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 3,
             "label": "杰青"},
            {"id": 34, "name": "李明", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 3,
             "label": "杰青"},
            {"id": 35, "name": "林元华", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 3,
             "label": "杰青"},
            {"id": 36, "name": "南策文", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 3,
             "label": "杰青"},
            {"id": 37, "name": "王秀梅", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 3,
             "label": "杰青"},
            {"id": 38, "name": "李龙土", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "杰青"},
            {"id": 39, "name": "李敬锋", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "院士"},
            {"id": 40, "name": "王轲", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "院士"},
            {"id": 41, "name": "李亮亮", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "院士"},
            {"id": 42, "name": "周济", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "院士"},
            {"id": 43, "name": "王晓慧", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "院士"},
            {"id": 44, "name": "褚祥诚", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "院士"},
            {"id": 45, "name": "李文珍", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "院士"},
            {"id": 46, "name": "李正操", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": "院士"},
            {"id": 47, "name": "林红", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 2,
             "label": "院士"},
            {"id": 48, "name": "马静", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 2,
             "label": "院士"},
            {"id": 49, "name": "唐子龙", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 2,
             "label": "杰青"},
            {"id": 50, "name": "凌云汉", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 2,
             "label": "杰青"},
            {"id": 51, "name": "徐贲", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 2,
             "label": "杰青"},
            {"id": 52, "name": "刘伟", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 2,
             "label": "杰青"},
            {"id": 53, "name": "韦进全", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 2,
             "label": "杰青"},
            {"id": 54, "name": "刘光华", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 2,
             "label": "杰青"},
            {"id": 55, "name": "许庆彦", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 2,
             "label": "杰青"},
            {"id": 56, "name": "韦丹", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 2,
             "label": "杰青"},
            {"id": 57, "name": "潘峰", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 2,
             "label": "杰青"},
            {"id": 58, "name": "吴晓东", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 2,
             "label": "杰青"},
            {"id": 59, "name": "翁端", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 2,
             "label": "杰青"},
            {"id": 60, "name": "苗伟", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 2, "label": ""},
            {"id": 61, "name": "宋成", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 2, "label": ""},
            {"id": 62, "name": "曾飞", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 2, "label": ""},
            {"id": 63, "name": "曾照强", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": ""},
            {"id": 64, "name": "司文捷", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 1,
             "label": ""},
            {"id": 65, "name": "伍晖", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 4, "label": ""},
            {"id": 66, "name": "冉锐", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 4, "label": ""},
            {"id": 67, "name": "赵凌云", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 4,
             "label": ""},
            {"id": 68, "name": "钟敏霖", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 4,
             "label": ""},
            {"id": 69, "name": "汪长安", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 4,
             "label": ""},
            {"id": 70, "name": "岳振星", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 4,
             "label": "杰青"},
            {"id": 71, "name": "庄大明", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 4,
             "label": "杰青"},
            {"id": 72, "name": "朱宏伟", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 5,
             "label": ""},
            {"id": 73, "name": "杨金龙", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 5,
             "label": ""},
            {"id": 74, "name": "张文征", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 5,
             "label": ""},
            {"id": 75, "name": "杨志刚", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 5,
             "label": ""},
            {"id": 76, "name": "于荣", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 5, "label": ""},
            {"id": 77, "name": "朱静", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 5, "label": ""},
            {"id": 78, "name": "钟虓龑", "code": "0805", "school": "清华大学", "insititution": "材料学院", "class": 5,
             "label": ""}],

        "links": [
            {"source": 1, "target": 0, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 2, "target": 1, "paper": 0, "patent": 1, "project": 1, "weight": 2, "label": "同事"},
            {"source": 4, "target": 3, "paper": 0, "patent": 6, "project": 0, "weight": 6, "label": "同事"},
            {"source": 5, "target": 4, "paper": 0, "patent": 2, "project": 0, "weight": 2, "label": "同事"},
            {"source": 6, "target": 4, "paper": 1, "patent": 11, "project": 2, "weight": 14, "label": "同事"},
            {"source": 8, "target": 7, "paper": 0, "patent": 18, "project": 0, "weight": 18, "label": "同事"},
            {"source": 9, "target": 8, "paper": 1, "patent": 18, "project": 1, "weight": 20, "label": "同事"},
            {"source": 10, "target": 8, "paper": 4, "patent": 15, "project": 1, "weight": 20, "label": "同事"},
            {"source": 12, "target": 11, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 14, "target": 13, "paper": 0, "patent": 2, "project": 0, "weight": 2, "label": "同事"},
            {"source": 15, "target": 14, "paper": 0, "patent": 1, "project": 0, "weight": 1, "label": "同事"},
            {"source": 16, "target": 14, "paper": 0, "patent": 3, "project": 0, "weight": 3, "label": "师徒"},
            {"source": 18, "target": 17, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "师徒"},
            {"source": 19, "target": 18, "paper": 0, "patent": 0, "project": 2, "weight": 2, "label": "师徒"},
            {"source": 20, "target": 18, "paper": 1, "patent": 0, "project": 0, "weight": 1, "label": "师徒"},
            {"source": 21, "target": 18, "paper": 1, "patent": 0, "project": 0, "weight": 1, "label": "师徒"},
            {"source": 23, "target": 22, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "师徒"},
            {"source": 23, "target": 3, "paper": 1, "patent": 0, "project": 0, "weight": 1, "label": "师徒"},
            {"source": 23, "target": 6, "paper": 1, "patent": 0, "project": 0, "weight": 1, "label": "师徒"},
            {"source": 24, "target": 11, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "师徒"},
            {"source": 25, "target": 11, "paper": 5, "patent": 0, "project": 3, "weight": 8, "label": "师徒"},
            {"source": 26, "target": 24, "paper": 0, "patent": 0, "project": 3, "weight": 3, "label": "师徒"},
            {"source": 25, "target": 24, "paper": 1, "patent": 0, "project": 1, "weight": 2, "label": "师徒"},
            {"source": 27, "target": 24, "paper": 1, "patent": 0, "project": 1, "weight": 2, "label": "师徒"},
            {"source": 13, "target": 0, "paper": 0, "patent": 2, "project": 0, "weight": 2, "label": "师徒"},
            {"source": 28, "target": 13, "paper": 3, "patent": 14, "project": 1, "weight": 18, "label": "师徒"},
            {"source": 16, "target": 13, "paper": 6, "patent": 23, "project": 4, "weight": 33, "label": "师徒"},
            {"source": 29, "target": 26, "paper": 5, "patent": 0, "project": 3, "weight": 8, "label": "师徒"},
            {"source": 16, "target": 0, "paper": 0, "patent": 1, "project": 0, "weight": 1, "label": "师徒"},
            {"source": 16, "target": 15, "paper": 0, "patent": 1, "project": 0, "weight": 1, "label": "师徒"},
            {"source": 28, "target": 16, "paper": 3, "patent": 14, "project": 1, "weight": 18, "label": "师徒"},
            {"source": 27, "target": 22, "paper": 0, "patent": 2, "project": 1, "weight": 3, "label": "师徒"},
            {"source": 26, "target": 22, "paper": 1, "patent": 0, "project": 1, "weight": 2, "label": "师徒"},
            {"source": 25, "target": 22, "paper": 2, "patent": 0, "project": 1, "weight": 3, "label": "师徒"},
            {"source": 31, "target": 30, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "师徒"},
            {"source": 32, "target": 31, "paper": 1, "patent": 0, "project": 4, "weight": 5, "label": "师徒"},
            {"source": 34, "target": 33, "paper": 0, "patent": 6, "project": 0, "weight": 6, "label": "同事"},
            {"source": 35, "target": 34, "paper": 0, "patent": 7, "project": 0, "weight": 7, "label": "同事"},
            {"source": 36, "target": 34, "paper": 0, "patent": 7, "project": 1, "weight": 8, "label": "同事"},
            {"source": 32, "target": 2, "paper": 0, "patent": 2, "project": 0, "weight": 2, "label": "同事"},
            {"source": 37, "target": 2, "paper": 1, "patent": 0, "project": 0, "weight": 1, "label": "同事"},
            {"source": 2, "target": 0, "paper": 1, "patent": 0, "project": 2, "weight": 3, "label": "同事"},
            {"source": 39, "target": 38, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 39, "target": 36, "paper": 0, "patent": 0, "project": 4, "weight": 4, "label": "同事"},
            {"source": 40, "target": 39, "paper": 1, "patent": 0, "project": 4, "weight": 5, "label": "同事"},
            {"source": 41, "target": 3, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 42, "target": 38, "paper": 0, "patent": 1, "project": 0, "weight": 1, "label": "同事"},
            {"source": 38, "target": 36, "paper": 0, "patent": 0, "project": 3, "weight": 3, "label": "同事"},
            {"source": 43, "target": 38, "paper": 0, "patent": 14, "project": 1, "weight": 15, "label": "同事"},
            {"source": 44, "target": 38, "paper": 5, "patent": 0, "project": 1, "weight": 6, "label": "同事"},
            {"source": 45, "target": 26, "paper": 1, "patent": 0, "project": 0, "weight": 1, "label": "同事"},
            {"source": 10, "target": 7, "paper": 6, "patent": 15, "project": 2, "weight": 23, "label": "同事"},
            {"source": 10, "target": 9, "paper": 9, "patent": 19, "project": 2, "weight": 30, "label": "同事"},
            {"source": 46, "target": 32, "paper": 0, "patent": 0, "project": 2, "weight": 2, "label": "同事"},
            {"source": 46, "target": 20, "paper": 2, "patent": 0, "project": 2, "weight": 4, "label": "同事"},
            {"source": 47, "target": 21, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 48, "target": 35, "paper": 0, "patent": 6, "project": 0, "weight": 6, "label": "同事"},
            {"source": 36, "target": 35, "paper": 0, "patent": 35, "project": 9, "weight": 44, "label": "同事"},
            {"source": 49, "target": 35, "paper": 1, "patent": 0, "project": 0, "weight": 1, "label": "同事"},
            {"source": 35, "target": 33, "paper": 1, "patent": 26, "project": 1, "weight": 28, "label": "同事"},
            {"source": 50, "target": 20, "paper": 0, "patent": 3, "project": 0, "weight": 3, "label": "同事"},
            {"source": 52, "target": 51, "paper": 0, "patent": 2, "project": 1, "weight": 3, "label": "同事"},
            {"source": 52, "target": 19, "paper": 0, "patent": 2, "project": 0, "weight": 2, "label": "同事"},
            {"source": 53, "target": 52, "paper": 0, "patent": 1, "project": 0, "weight": 1, "label": "同事"},
            {"source": 52, "target": 48, "paper": 0, "patent": 4, "project": 0, "weight": 4, "label": "同事"},
            {"source": 9, "target": 7, "paper": 5, "patent": 24, "project": 1, "weight": 30, "label": "同事"},
            {"source": 54, "target": 51, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 32, "target": 30, "paper": 0, "patent": 0, "project": 3, "weight": 3, "label": "同事"},
            {"source": 27, "target": 26, "paper": 0, "patent": 3, "project": 0, "weight": 3, "label": "同事"},
            {"source": 55, "target": 26, "paper": 2, "patent": 0, "project": 3, "weight": 5, "label": "同事"},
            {"source": 26, "target": 25, "paper": 3, "patent": 0, "project": 2, "weight": 5, "label": "同事"},
            {"source": 32, "target": 20, "paper": 0, "patent": 0, "project": 3, "weight": 3, "label": "同事"},
            {"source": 56, "target": 32, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 57, "target": 32, "paper": 1, "patent": 0, "project": 2, "weight": 3, "label": "同事"},
            {"source": 28, "target": 0, "paper": 0, "patent": 1, "project": 0, "weight": 1, "label": "同事"},
            {"source": 48, "target": 33, "paper": 0, "patent": 2, "project": 0, "weight": 2, "label": "同事"},
            {"source": 48, "target": 40, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 48, "target": 36, "paper": 0, "patent": 7, "project": 4, "weight": 11, "label": "同事"},
            {"source": 58, "target": 48, "paper": 1, "patent": 0, "project": 1, "weight": 2, "label": "同事"},
            {"source": 59, "target": 48, "paper": 1, "patent": 0, "project": 1, "weight": 2, "label": "同事"},
            {"source": 60, "target": 20, "paper": 0, "patent": 0, "project": 3, "weight": 3, "label": "同事"},
            {"source": 61, "target": 57, "paper": 6, "patent": 32, "project": 2, "weight": 40, "label": "同事"},
            {"source": 62, "target": 57, "paper": 3, "patent": 63, "project": 2, "weight": 68, "label": "同事"},
            {"source": 63, "target": 21, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 64, "target": 21, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 59, "target": 21, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 21, "target": 15, "paper": 1, "patent": 11, "project": 6, "weight": 18, "label": "同事"},
            {"source": 21, "target": 17, "paper": 2, "patent": 1, "project": 1, "weight": 4, "label": "同事"},
            {"source": 65, "target": 21, "paper": 2, "patent": 0, "project": 1, "weight": 3, "label": "同事"},
            {"source": 21, "target": 20, "paper": 1, "patent": 0, "project": 0, "weight": 1, "label": "同事"},
            {"source": 64, "target": 15, "paper": 0, "patent": 1, "project": 0, "weight": 1, "label": "同事"},
            {"source": 63, "target": 15, "paper": 0, "patent": 1, "project": 0, "weight": 1, "label": "同事"},
            {"source": 66, "target": 59, "paper": 5, "patent": 20, "project": 1, "weight": 26, "label": "同事"},
            {"source": 66, "target": 58, "paper": 4, "patent": 20, "project": 2, "weight": 26, "label": "同事"},
            {"source": 5, "target": 3, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 6, "target": 3, "paper": 3, "patent": 14, "project": 2, "weight": 19, "label": "同事"},
            {"source": 36, "target": 33, "paper": 0, "patent": 34, "project": 0, "weight": 34, "label": "同事"},
            {"source": 51, "target": 33, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 27, "target": 25, "paper": 2, "patent": 0, "project": 0, "weight": 2, "label": "同事"},
            {"source": 64, "target": 63, "paper": 0, "patent": 1, "project": 0, "weight": 1, "label": "同事"},
            {"source": 64, "target": 19, "paper": 0, "patent": 0, "project": 2, "weight": 2, "label": "同事"},
            {"source": 62, "target": 61, "paper": 1, "patent": 16, "project": 0, "weight": 17, "label": "同事"},
            {"source": 37, "target": 0, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 67, "target": 0, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 59, "target": 0, "paper": 1, "patent": 0, "project": 0, "weight": 1, "label": "同事"},
            {"source": 58, "target": 0, "paper": 1, "patent": 0, "project": 0, "weight": 1, "label": "同事"},
            {"source": 49, "target": 20, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 69, "target": 68, "paper": 0, "patent": 1, "project": 0, "weight": 1, "label": "同事"},
            {"source": 69, "target": 36, "paper": 0, "patent": 0, "project": 3, "weight": 3, "label": "同事"},
            {"source": 51, "target": 40, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 43, "target": 36, "paper": 0, "patent": 0, "project": 3, "weight": 3, "label": "同事"},
            {"source": 70, "target": 43, "paper": 1, "patent": 0, "project": 0, "weight": 1, "label": "同事"},
            {"source": 43, "target": 42, "paper": 2, "patent": 0, "project": 0, "weight": 2, "label": "同事"},
            {"source": 71, "target": 53, "paper": 0, "patent": 3, "project": 0, "weight": 3, "label": "同事"},
            {"source": 72, "target": 53, "paper": 0, "patent": 15, "project": 0, "weight": 15, "label": "同事"},
            {"source": 59, "target": 58, "paper": 9, "patent": 29, "project": 2, "weight": 40, "label": "同事"},
            {"source": 73, "target": 19, "paper": 4, "patent": 0, "project": 1, "weight": 5, "label": "同事"},
            {"source": 55, "target": 25, "paper": 2, "patent": 0, "project": 0, "weight": 2, "label": "同事"},
            {"source": 74, "target": 51, "paper": 0, "patent": 0, "project": 2, "weight": 2, "label": "同事"},
            {"source": 75, "target": 74, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 6, "target": 5, "paper": 0, "patent": 2, "project": 0, "weight": 2, "label": "同事"},
            {"source": 76, "target": 36, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 77, "target": 76, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 70, "target": 36, "paper": 0, "patent": 0, "project": 3, "weight": 3, "label": "同事"},
            {"source": 70, "target": 42, "paper": 8, "patent": 0, "project": 0, "weight": 8, "label": "同事"},
            {"source": 36, "target": 20, "paper": 0, "patent": 0, "project": 1, "weight": 1, "label": "同事"},
            {"source": 78, "target": 77, "paper": 1, "patent": 2, "project": 3, "weight": 6, "label": "同事"},
            {"source": 42, "target": 36, "paper": 0, "patent": 0, "project": 4, "weight": 4, "label": "同事"},
            {"source": 72, "target": 71, "paper": 0, "patent": 2, "project": 0, "weight": 2, "label": "同事"},
            {"source": 44, "target": 36, "paper": 0, "patent": 0, "project": 3, "weight": 3, "label": "同事"}
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
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


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

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(debug=True)
