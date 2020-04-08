import os

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_session import Session
import json
from classes import (
    Channel,
    Message,
    User
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234567890"
app.config["SESSION_TYPE"] = "filesystem"
SESSION_TYPE = 'filesystem'
socketio = SocketIO(app)
Session(app)

# 当前频道列表
channels = []
# 当前用户列表
users = []


channels.append(Channel(index=0, name="First"))
channels.append(Channel(index=1, name="Second"))

channels[0].add_message(Message(User("", "Admin", 0), "Test"))



@app.route("/", methods=["GET", "POST"])
def index():
    # 显示index页面
    if request.method == "GET":
        return render_template("index.html", channels=channels)
    # 处理登入信息
    else:
        # 创建一个user类
        u_name = request.form.get("nickname")
        print('|||||||||||||'+request.args.get("t"))
        new_user = User(request.args.get("t"), u_name, None)
        # 如果当前用户列表中存在该用户，则返回原处，并提示
        if new_user.name in [u.name for u in users]:
            flash("The user name is already used!")
            return redirect("/", "303")
        # 设置当前会话的用户信息，返回频道列表
        session["user"] = u_name
        session["channel"] = None
        return redirect("/channels")


@app.route("/channels", methods={"GET"})
def channels_view():
    # 已经注册过
    if session.get("user"):
        u_name = session["user"]
        # 用户点击特定频道，将该频道与用户绑定
        if request.args.get("ch"):
            new_channel = int(request.args.get("ch"))
            session["channel"] = new_channel
            return redirect("/channel")
        else:
            return render_template("channels.html", channels=channels, user=u_name)
    # 若尚未注册，返回、报错
    else:
        flash("Not log in!")
        return redirect("/", "303")


@app.route("/channel")
def channel_view():
    # 已经注册过
    if session.get("user"):
        u_name = session["user"]
        # 此时接收到由/channels路由处绑定的用户频道
        u_channel = session["channel"]
        # 返回改频道的所有消息及用户
        return render_template("channel.html", channel=channels[u_channel], user=u_name, prev_user="None")
    # 若尚未注册，返回、报错
    else:
        flash("You are not logged")
        return redirect("/", "303")


@app.route("/create_channel", methods=["GET", "POST"])
def create_channel():
    if request.method == "GET":
        return render_template("create_channel.html")
    else:
        # 已经注册过
        if session.get("user"):
            # POST方法提交建立频道名称
            new_channel_name = request.form.get("channel_name")
            new_channel = Channel(index=len(channels), name=new_channel_name)
            # 如果当前频道列表中存在该频道，则返回原处，并提示
            if new_channel.name in [c.name for c in channels]:
                flash("The user name is already used!")
                return redirect("/create_channel", "303")
            channels.append(new_channel)
            flash("Channel created successfully")
            return redirect("/channels")
        # 若尚未注册，返回、报错
        else:
            flash("You are not logged")
            return redirect("/", "303")


if __name__ == '__main__':
    app.run()
