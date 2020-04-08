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

channels.append(Channel(index=0, name="第一组"))
channels.append(Channel(index=1, name="第二组"))
channels.append(Channel(index=2, name="第三组"))
channels.append(Channel(index=3, name="第四组"))
channels.append(Channel(index=4, name="第五组"))
channels.append(Channel(index=5, name="第六组"))
channels.append(Channel(index=6, name="第七组"))
channels.append(Channel(index=7, name="第八组"))
channels.append(Channel(index=8, name="第九组"))
channels.append(Channel(index=9, name="第十组"))

channels[0].add_message(Message(User("Admin", 0), "Test"))


@app.route("/", methods=["GET", "POST"])
def index():
    # 显示index页面
    if request.method == "GET":
        return render_template("index.html")
    # 处理登入信息
    else:
        # 创建一个user类
        u_name = request.form.get("nickname")
        new_user = User(u_name, 0)
        # 如果当前用户列表中存在该用户，则返回原处，并提示
        if request.form.get("nickname") in [u.name for u in users]:
            flash("The user name is already used!")
            return redirect("/", "303")
        # 设置当前会话的用户信息，返回频道列表
        session["user"] = u_name
        session["channel"] = 0
        users.append(new_user)
        print('登入！当前用户：', users)
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
            # index递增
            new_channel = Channel(index=len(channels), name=new_channel_name)
            # 如果当前频道列表中存在该频道，则返回原处，并提示
            if new_channel.name in [c.name for c in channels]:
                flash("The channel name is already used!")
                return redirect("/create_channel", "303")
            channels.append(new_channel)
            flash("Channel created successfully")
            return redirect("/channels")
        # 若尚未注册，返回、报错
        else:
            flash("Not log in！")
            return redirect("/", "303")


@app.route("/logout")
def logout():
    try:
        del_user = User(session['user'], session["channel"])
        del_from = Channel(session["channel"], 0)
    except KeyError:
        return redirect("/", "303")
    try:
        users.remove(del_user)
        channels[channels.index(del_from)].users.remove(session['user'])
    except ValueError:
        pass
    session.clear()
    print('登出！当前用户：', users)
    return redirect("/")


@socketio.on("register_on_channel")
def select_channel(data):
    u_name = data["nickname"]
    u_channel = int(data["channel"])
    print(u_name, u_channel)
    join_room(u_channel)
    # 防止重复添加
    if u_name not in channels[u_channel].users:
        channels[u_channel].users.append(u_name)
    # 更新并广播
    nickname_array = json.dumps(channels[u_channel].users)
    print(nickname_array)
    emit("current_client_list", {"users": nickname_array}, room=u_channel)


@socketio.on("new_message")
def new_message(data):
    u_name = data["nickname"]
    u_channel = int(data["channel"])
    user = User(u_name, u_channel)
    print(u_name, u_channel)
    if user in users:
        join_room(u_channel)
        text = data["message"]
        msg = Message(user, text)
        channels[u_channel].add_message(msg)
        print("receivde msg:", text, "from", u_name)
        emit("write_message", {
            "nickname": u_name,
            "message": text
        }, room=u_channel)
    else:
        print('未登录！')


@socketio.on('connect')
def connect():
    print("Client connected", request.args.get("t"))


@socketio.on('disconnect')
def disconnect():
    try:
        del_user = User(session['user'], session["channel"])
        del_from = Channel(session["channel"], 0)
        try:
            channels[channels.index(del_from)].users.remove(session['user'])
        except ValueError:
            pass
        nickname_array = json.dumps(channels[session["channel"]].users)
        print(nickname_array)
        emit("current_client_list", {"users": nickname_array}, room=session["channel"])
        print('掉线: ', session['user'])
    except KeyError:
        pass
    session.clear()


if __name__ == '__main__':
    app.run()
