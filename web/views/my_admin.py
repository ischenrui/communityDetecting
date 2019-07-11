from flask import Flask, render_template, redirect, session, request, Blueprint
import logging, json, os
import sys
from urllib import parse

from service.adminServer import admin_service

sys.path.append("..")

my_admin = Blueprint('my_admin', __name__)


@my_admin.route('/admin')
def admin_index():
    return render_template('admin.html')


@my_admin.route('/admin/add')
def admin_add():
    return render_template('admin_add.html')


@my_admin.route('/admin/accounts')
def admin_list():
    return render_template('admin_accounts.html')


@my_admin.route('/admin/setting-spider')
def admin_spider_setting():
    return render_template('admin_spider.html')


@my_admin.route('/admin/data')
def admin_data():
    return render_template('admin_data.html')


@my_admin.route('/admin/logging')
def admin_logging():
    return render_template('admin_logging.html')

#
# @my_admin.route('/test')
# def admin_test():
#     return render_template('test.html')


@my_admin.route('/logging/getdata', methods=['GET', 'POST'])
def get_logging():
    t = request.form.get('data')
    data = json.loads(t)

    result = admin_service.get_web_log(data)

    ajax = dict()
    ajax['success'] = True
    ajax['msg'] = ''
    ajax['obj'] = result
    s = json.dumps(ajax)
    return s


@my_admin.route('/add/insert', methods=['GET', 'POST'])
def insert_account():

    account = request.form.get('account')
    name = request.form.get('name')
    password = request.form.get('password')
    type_ = request.form.get('type')

    this_account = "admin"

    params = (account, name, password, type_, this_account)

    result = admin_service.insert_account(params)

    ajax = dict()
    if result == 1:
        ajax['success'] = True
        ajax['msg'] = ''
    elif result == 1062:

        ajax['success'] = False
        ajax['msg'] = "账号已被注册"
    else:
        ajax['success'] = False
        ajax['msg'] = "未成功添加，请重新输入"
    ajax['obj'] = ""
    s = json.dumps(ajax)
    return s


@my_admin.route('/add/data', methods=['GET', 'POST'])
def get_latest_accounts():
    # create_account = session["account"]
    create_account = "admin"
    print(create_account)

    result = admin_service.get_latest_accounts(create_account)

    ajax = dict()
    ajax['success'] = True
    ajax['msg'] = ''
    ajax['obj'] = result
    s = json.dumps(ajax)
    return s


@my_admin.route('/accounts/list', methods=['GET', 'POST'])
def get_accounts():
    t = request.form.get('data')
    params = json.loads(t)
    print(params)
    result = admin_service.get_accounts(params)

    ajax = dict()
    ajax['success'] = True
    ajax['msg'] = ''
    ajax['obj'] = result
    s = json.dumps(ajax)
    return s


@my_admin.route('/accounts/delete', methods=['GET', 'POST'])
def delete_account():
    t = json.loads(request.form.get('data'))
    params = t['id']
    print(params)
    result = admin_service.delete_account(params)

    ajax = dict()
    if result == 1:
        ajax['success'] = True
        ajax['msg'] = ''
    else:
        ajax['success'] = False
        ajax['msg'] = "插入失败"
    ajax['obj'] = result
    s = json.dumps(ajax)
    return s


@my_admin.route('/accounts/update', methods=['GET', 'POST'])
def update_account():
    _id = request.form.get("id")
    name = request.form.get("name")
    password = request.form.get("password")
    status = request.form.get("type")
    status = parse.unquote(status)
    params = (name, password, status, _id)
    result = admin_service.update_account(params)

    ajax = dict()
    if result == 1:
        ajax['success'] = True
        ajax['msg'] = ''
    elif result == 0:
        ajax['success'] = False
        ajax['msg'] = "未修改内容"
    else:
        ajax['success'] = False
        ajax['msg'] = "更新失败"
    ajax['obj'] = {}
    s = json.dumps(ajax)
    return s
