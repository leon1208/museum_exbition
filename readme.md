<p align="center">
	<!-- <img alt="logo" src="https://oscimg.oschina.net/oscnet/up-d3d0a9303e11d522a06cd263f3079027715.png"> -->
</p>
<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">展慧博物馆管理系统</h1>
<h4 align="center"></h4>
<p align="center">
	<a href="https://gitee.com/shaw-lee/ruoyi-vue-flask/blob/5139e50de7a5d97e0a512019e87a0961768ec9aa/LICENSE"><img src="https://img.shields.io/github/license/mashape/apistatus.svg"></a>
</p>


## 平台简介

本项目基于若依的Flask+Vue前后端分离的版本进行开发，给个人及企业免费使用。因为我个人接的一些项目实现了博物馆和展览中一些常用的功能，所以我想把这些功能集成到一起，形成一个简单的产品。

* 前端后端的技术栈沿用若依的Flask+Vue
  * 后端增加了对alembic的迁移脚本管理框架的支持，参考migrations文件夹下的readme文件。
  * 后端增加了对容器化部署的支持，参考docker文件夹。
  * 后端增加了对minio的支持。
  * 前端增加了对小程序的支持。
* 环境管理，后端调整为uv进行环境管理，前端使用volta和pnpm进行依赖管理。
* 特别鸣谢： [Ruoyi-Vue (V3.8.1)](https://gitee.com/y_project/RuoYi-Vue) https://gitee.com/shaw-lee/ruoyi-vue-flask


## 主要功能

若依框架原有的功能全部保留，和博物馆展览相关的功能如下，我将陆续实现，也可能在实现过程中对进行调整：
1.  博物馆管理：博物馆是系统操作者，该功能主要完成博物馆的基本配置和展厅的配置。
2.  展览管理：展览是博物馆的一个子模块，主要完成展览的配置，包括展览的时间、地点、展览的藏品等。
3.  藏品管理：藏品是展览的一个子模块，主要完成展览中的藏品的配置，包括藏品的名称、描述、图片等。
4.  展览导览：根据展览的藏品生成文字和语音讲解，为观众提供小程序端的导览服务。
5.  教育活动：配置博物馆的公共教育活动，提供活动一些周边物料管理、预约报名功能。

其他功能设想：
* 展览大纲设计：根据展览的主题、藏品等信息，通过AI辅助展览大纲的编写。
* 展览活动宣传：根据展览或者活动的已经录入的信息，通过AI辅助生成宣传用的图片和文字。
* 自动语音导览：配合蓝牙室内定位，根据用户的位置和导览路径，自动播放导览语音。
* 在线展览：可将展览的720全景应用上传至平台，用户可在小程序端查看和播放，实现永不落幕的展览。

## 安装部署

### 软件版本

```text
本项目python和node的版本管理使用uv和volta，分别管理python和node的版本。
python版本：3.13+
mysql版本：8+
redis版本：8+
node版本：v20.17.0

工程的版本号在根目录下文件：./VERSION
```

### mysql数据库
```text
可参考migrations文件夹下的readme文件进行数据库迁移。
```
### 后端快速启动

```cmd
# 安装uv
pipx install uv

# 进入项目目录，创建虚拟环境
uv sync

# 激活虚拟环境
source ./.venv/bin/activate
```

```text
# 后端配置，注意不要提交.env文件
cp ./ruoyi_admin/config/env.example ./ruoyi_admin/config/.env

# 调整.env文件，根据实际情况修改数据库连接信息、redis连接信息等。
# 也可以根据项目情况调整app.yml文件，例如修改上传文件的路径等。
```

```cmd
# 启动服务
python ruoyi_admin/app.py
```

### 前端快速启动

```cmd
# 安装依赖, 推荐使用volta, 安装node版本为v20.17.0
volta install node@20.17.0
volta install pnpm

cd ruoyi-ui
pnpm install

# 启动服务
pnpm run dev
```

### 浏览器访问
```text
地址: http://localhost:1024
用户名/密码: admin/admin123
```

### 容器化部署
```text
# 1.自行部署mysql、redis、minio等服务。
# 2.修改./ruoyi_admin/config/.env文件，根据部署实际部署修改数据库连接信息、redis连接信息等。该文件在开发、测试和生产环境中都需要修改，不建议在代码仓库中提交该文件。
# 3.利用./docker/runbuild.sh中的命令编译镜像

## 编译,在项目根目录下执行
APP_VERSION=$(cat VERSION) docker-compose -f docker/docker-compose.yaml build

## 编译加启动,在项目根目录下执行
APP_VERSION=$(cat VERSION) docker-compose -f docker/docker-compose.yaml up -d --build
```