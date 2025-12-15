# ====================== 前端Nginx镜像构建 ======================
FROM node:20.17-alpine AS frontend-builder
WORKDIR /app

# 安装pnpm
RUN npm install -g pnpm

# 复制前端代码
COPY ruoyi-ui /app

# 使用pnpm安装依赖并构建前端
RUN pnpm install && pnpm run build:prod

# 前端运行镜像：使用Nginx
FROM nginx:alpine AS frontend-nginx
WORKDIR /usr/share/nginx/html

# 复制Nginx配置文件
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

# 复制前端构建产物到Nginx
COPY --from=frontend-builder /app/dist /usr/share/nginx/html

# 暴露端口
EXPOSE 80

# ====================== 后端Flask镜像构建 ======================
FROM python:3.13-alpine AS backend-builder
WORKDIR /app

# 安装系统依赖
RUN apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    mariadb-dev \
    libffi-dev \
    openssl-dev \
    make \
    git

# 安装uv
RUN pip install --upgrade pip && pip install uv

# 复制项目文件
COPY . /app

# 使用uv安装依赖
RUN uv install -r bin/requirements.txt

# 后端运行镜像
FROM python:3.13-alpine AS backend-runtime
WORKDIR /app

# 安装系统依赖
RUN apk add --no-cache \
    mariadb-connector-c \
    openssl \
    redis

# 安装uv
RUN pip install --upgrade pip && pip install uv

# 复制后端代码
COPY --from=backend-builder /app /app
COPY --from=backend-builder /root/.cache/uv /root/.cache/uv

# 设置环境变量
ENV PYTHONPATH=/app
ENV FLASK_APP=ruoyi_admin/app.py
ENV FLASK_ENV=production

# 暴露端口
EXPOSE 9000

# 运行应用
CMD ["python", "ruoyi_admin/app.py"]