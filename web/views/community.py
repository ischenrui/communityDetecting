from flask import Flask, render_template, redirect, request ,Blueprint

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField
from wtforms.validators import DataRequired,Required

community = Blueprint('community', __name__)



@community.route('/community',methods=['GET','POST'])
def community_index():

    return render_template('community_index.html')


