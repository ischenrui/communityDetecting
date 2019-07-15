from flask import Flask, render_template, redirect, session, request, Blueprint
import logging, json, os
import sys
from urllib import parse

from service.adminServer import admin_service
from web.views.login import is_login

sys.path.append("..")

my_admin = Blueprint('my_admin', __name__)


@my_admin.route('/admin')
@is_login
def admin_index():
    return render_template('admin.html')


@my_admin.route('/admin/add')
@is_login
def admin_add():
    return render_template('admin_add.html')


@my_admin.route('/admin/accounts')
@is_login
def admin_list():
    return render_template('admin_accounts.html')


@my_admin.route('/admin/setting-spider')
@is_login
def admin_spider_setting():
    re = admin_service.get_progressbar()
    return render_template('admin_spider.html', progressbar_now=re)


@my_admin.route('/admin/data')
@is_login
def admin_data():
    return render_template('admin_data.html')


@my_admin.route('/admin/logging')
@is_login
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


@my_admin.route('/spider/params', methods=['GET', 'POST'])
def get_params():
    ajax = dict()
    ajax['success'] = True
    ajax['msg'] = ''
    ajax['obj'] = eval(open('.\\static\\setting_data\\setting.txt', 'r', encoding='utf8').read())
    s = json.dumps(ajax)
    return s


@my_admin.route('/spider/save', methods=['GET', 'POST'])
def params_save():

    delay = request.form.get("delay")
    max_req = request.form.get("max_req")
    proxy = request.form.get("proxy")
    re_req = request.form.get("re_req")
    cookie = request.form.get("cookie")

    p_dict = dict()
    p_dict["DOWNLOAD_DELAY"] = int(delay)
    p_dict["CONCURRENT_REQUESTS"] = int(max_req)
    p_dict["PROXY_ENABLED"] = True if proxy == "on" else False
    p_dict["RE_REQUEST_ENABLED"] = True if re_req == "on" else False
    p_dict["COOKIES_ENABLED"] = True if cookie == "on" else False

    ajax = dict()
    try:
        print(p_dict)
        f = open('.\\static\\setting_data\\setting.txt', 'w', encoding='utf8')
        f.write(str(p_dict))
        f.close()
        ajax['success'] = True
        ajax['msg'] = ''
    except Exception as e:
        ajax['success'] = False
        ajax['msg'] = str(e)
    ajax['obj'] = p_dict
    s = json.dumps(ajax)
    return s


@my_admin.route('/spider/data', methods=['POST'])
def spider_log():
    t = request.form.get('data')
    params = json.loads(t)
    print(params)
    result = admin_service.get_spider_log(params)

    ajax = dict()
    ajax['success'] = True
    ajax['msg'] = ''
    ajax['obj'] = result
    s = json.dumps(ajax)
    return s
    pass


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
        ajax['msg'] = "删除失败"
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
