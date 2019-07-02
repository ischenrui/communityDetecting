from flask import Flask, render_template, redirect, request, Blueprint
import logging, json, os
import sys
sys.path.append("..")

my_admin = Blueprint('my_admin', __name__)


@my_admin.route('/admin')
def admin_index():
    return render_template('admin.html')


@my_admin.route('/admin/add')
def admin_add():
    return render_template('form_component.html')

