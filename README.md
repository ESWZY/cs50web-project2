# Project 2

Web Programming with Python and JavaScript

# 介绍

这是课程 CS50 Web Programming with Python and JavaScript 的 project 2。
主要目的是按照特定的要求模仿 Flack，设计一个广播群组频道网站。详细要求见 [`Requirements.md`](https://github.com/ESWZY/cs50web-project2) 。

# 安装并运行

首先选择位置启动 git 命令行，执行 `git clone https://github.com/ESWZY/cs50web-project2.git` ，或者也可以点击右上角的绿色按钮 `Clone or download` ，并选择相应选项下载源代码。

随后进入程序主目录，安装相关的依赖库`pip install -r requirements.txt` 。

随后设置环境变量：

对于 Mac 或 Linux，执行 `export FLASK_APP=app.py` ，对于 Windows，执行 `set FLASK_APP=application.py`

最后执行 `flask run` 即可成功执行，打开 http://127.0.0.1:5000/ 即可。

# 文件结构

- `lecture 5 ~ 7` 是课程中用到的的教学源代码。

- `static` 目录是项目用到的 CSS 文件、 JS 文件和图片等静态文件。

- `templates` 目录是 Flack 服务器使用的 HTML 模板文件。

- `screenshot` 目录包含了项目的截屏图片。

- `classes.py` 包含了程序中使用到的一些类。

- `app.py` 是应用程序的主文件。

- 其余文件均为杂项文件。

# 流程及界面

## 布局

整体页面布局分为三个部分：顶部导航栏、中部内容区和底部页脚栏。页面布局如下图所示。

![img](/screenshot/1.png)

- 顶部导航栏左侧包含了主要的功能导航按钮，右侧包含了登入按钮，且如果已经登录，还会显示用户名和登出按钮。如下图所示。

- 中部内容区为主要功能逻辑的展示区。

- 底部页脚栏包含了项目简介，快速导航栏和反馈方式。

## 登录

登录界面如下图所示。在登录主界面的输入框中输入登录用户名即可完成登录。如果当前用户已经存在，则会提示“该名称已被使用”。

![img](/screenshot/2.png)

## 频道列表

在登录成功之后，网页会定向到频道列表，展示当前存在的所有频道。界面如下图所示。

![img](/screenshot/3.png)

## 频道

在频道列表点击一个频道进入后，就进入了频道界面。界面左侧是当前在频道内的用户，右侧为消息交互窗口。界面如下图所示。

![img](/screenshot/4.png)

## 创建频道

在上方导航栏内，点击“创建频道”按钮，即可进入创建频道界面。在输入框中输入频道名称，点击“提交”，即可创建成功。创建频道界面，以及创建成功的结果如下图所示。

![img](/screenshot/5.png)

![img](/screenshot/6.png)

# 特点和功能

- 重复创建用户名/频道名会提示该名称已存在。

- 任意用户名登录，任意频道名，无语言编码问题。

- 随机的频道列表表项的颜色。

- 服务器端为每个频道保存100条消息。

- 浏览器记录当前所在的频道，在重新打开网页时仍在该频道。

- 消息界面着重提示当前用户。

- 强制登出。

消息发送界面如下图所示。

![img](/screenshot/7.png)

![img](/screenshot/8.png)

![img](/screenshot/9.png)

