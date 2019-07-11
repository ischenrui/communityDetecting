from flask import Flask, render_template, redirect, request ,Blueprint

import json
# from dbhelper import DBConnecter as DB
from db.mydba import db_crpc

community = Blueprint('community', __name__)


@community.route('/community', methods=['GET', 'POST'])
def community_index():
    school = [_['SCHOOL_NAME'] for _ in get_school_list()]
    institution = [_['NAME'] for _ in get_institution_list(school[0])]

    return render_template('community_index.html', school=school, institution=institution, selected_s=school[0], selected_i=institution[0])


@community.route('/institution', methods=['GET', 'POST'])
def get_institution():
    school = request.args.get("school")
    # return json.dumps(tuple_2_list(get_institution_list(school)))
    return json.dumps([_['NAME'] for _ in get_institution_list(school)])


def get_school_list():
    # school = DB.execute("select SCHOOL_NAME from es_institution group by SCHOOL_NAME ORDER BY SCHOOL_NAME DESC")
    sql = "select SCHOOL_NAME from es_institution group by SCHOOL_NAME ORDER BY SCHOOL_NAME DESC"
    school = db_crpc.getDics(sql)
    return school


def get_institution_list(school):
    # institution = DB.execute("select NAME from es_institution where SCHOOL_NAME = '%s' and (DFC_NUM >0 or NKD_NUM>0 or SKL_NUM>0 or ACADEMICIAN_NUM>0)" % school)
    sql = "select NAME from es_institution where SCHOOL_NAME = '%s' " % school
    institution = db_crpc.getDics(sql)
    return institution


if __name__ == '__main__':

    a = get_institution_list("清华大学")
    print([_['NAME'] for _ in get_institution_list("清华大学")])

    # print(json.dumps(tuple_2_list(d)))