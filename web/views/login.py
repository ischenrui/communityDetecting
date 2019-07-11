from flask import Flask, render_template, redirect, request, session, Blueprint
import logging, json, os
import sys

# from service.adminServer import admin_service
from service.userServer import user_service

sys.path.append("..")

login = Blueprint('login', __name__)


@login.route('/login')
def login_form():
    return render_template('login.html')


@login.route('/login/check', methods=['GET', 'POST'])
def login_check():
        account = request.form.get('account')
        password = request.form.get('password')
        # m = hashlib.md5()
        # m.update(bytes(password, encoding="utf8"))
        # password = m.hexdigest()
        param = (account,)
        print(account, password)
        user = user_service.get_user(param)
        print(user)
        if user and user['psd'] == password:
            session['username'] = user['name']
            session['account'] = user['id']
            # ---cookie时间---
            session.permanent = True
            ajax = dict()
            ajax['success'] = True
            ajax['msg'] = ''
            ajax["obj"] = {"account": user['id']}
            s = json.dumps(ajax)
            return s
        else:
            ajax = dict()
            ajax['success'] = False
            ajax['msg'] = '此账号不存在' if not user else '密码错误'
            ajax["obj"] = {}
            s = json.dumps(ajax)
            return s


@login.route('/login/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    ajax = dict()
    ajax['success'] = True
    ajax['msg'] = ''
    ajax["obj"] = {}
    s = json.dumps(ajax)
    return s
