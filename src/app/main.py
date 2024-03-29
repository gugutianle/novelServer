#!/usr/bin/python
#coding=utf-8
import time
from logging import FileHandler,WARNING,DEBUG
from random import random
from os import urandom
from math import ceil

from flask import Flask,request,render_template,jsonify,redirect,url_for,make_response,g,send_from_directory
from flask import session as flaskSession
from flask_cors import CORS
from sqlalchemy import distinct,desc

from blueprint.home import homeBlueprint
from blueprint.user import userBlueprint
from blueprint.message import messageBlueprint
from blueprint.search import searchBlueprint
from blueprint.comment import commentBlueprint
from blueprint.collect import collectBlueprint

from model.base import Session

def create_app():
    app = Flask(__name__)
    app.secret_key = '\x14:\xe3\x1aB\xc5|\x10iQ\xd9 \xdf\xce\x19\x83\xd3\xb7s\x97\xee(T\xb8\xb25\xd3\xd1\xe1NJ\x92'
    CORS(app, supports_credentials=True, origins=['http://localhost:8080','http://localhost:3000'])

    # 日志记录
    fileHandler = FileHandler('/tmp/warning.log')
    fileHandler.setLevel(WARNING)
    app.logger.addHandler(fileHandler)

    # 注册蓝图
    app.register_blueprint(homeBlueprint)
    app.register_blueprint(userBlueprint)
    app.register_blueprint(messageBlueprint)
    app.register_blueprint(searchBlueprint)
    app.register_blueprint(commentBlueprint)
    app.register_blueprint(collectBlueprint)

    @app.before_request
    def before_request():
        g.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        g.expires = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()+86400))
        g.dbSession = Session()
        path = request.path
        if ('/logout' in path or '/changePassword' in path or '/user' in path) and ('username' not in flaskSession and request.cookies.get('username') != flaskSession['username']):
            return jsonify({
                'status': 'fail',
                'msg': '请先登录'
            })

    @app.teardown_request
    def teardown_request(exception):
        g.dbSession.close()

    @app.route('/search')
    def search():
        return redirect(url_for('search.search'))

    @app.route('/novel/list/<int:novelNum>')
    def novelList(novelNum):
        return redirect(url_for('home.novelList'))

    @app.route('/shelf')
    def shelf():
        return redirect(url_for('home.shelf'))

    @app.route('/novel/<int:id>')
    def novel(id):
        return redirect(url_for('home.novel'))

    @app.route('/novel/<int:id>/<int:charptId>')
    def charpt(id, charptId):
        return redirect(url_for('home.charpt'))

    @app.route('/collect/<int:novelId>')
    def collectNovel(novelId):
        return redirect(url_for('collect.collectNovel'))

    @app.route('/user/comment/<int:userId>')
    def userComment(userId):
        return redirect(url_for('comment.userComment'))

    @app.route('/comment/<int:novelId>')
    def comment(novelId):
        return redirect(url_for('comment.comment'))

    @app.route('/user/message/<int:userId>')
    def userMessage(userId):
        return redirect(url_for('message.userMessage'))

    @app.route('/message/<int:userId>')
    def message(userId):
        return redirect(url_for('message.message'))

    @app.route('/user/<int:userId>')
    def userInfo(userId):
        return redirect(url_for('user.userInfo'))

    @app.route('/register')
    def register():
        return redirect(url_for('user.register'))

    @app.route('/login')
    def login():
        return redirect(url_for('user.login'))

    @app.route('/logout')
    def logout():
        return redirect(url_for('user.logout'))

    @app.route('/changePassword')
    def changePassword():
        return redirect(url_for('user.changePassword'))

    return app
