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
FROM python:3.13-slim AS backend-builder
WORKDIR /app

# 安装 uv（官方二进制，非常快）
RUN pip install --no-cache-dir uv -i https://mirrors.aliyun.com/pypi/simple
#
# # 只复制依赖描述文件（最大化缓存）
COPY pyproject.toml uv.lock ./
#
# # 安装依赖到系统环境（不创建 venv）
RUN uv sync --frozen --no-dev --index https://mirrors.aliyun.com/pypi/simple


# 后端运行镜像
FROM python:3.13-slim AS backend-runtime
WORKDIR /app

# 从 builder 拷贝已安装的 site-packages
# COPY --from=backend-builder /usr/local/lib/python3.13 /usr/local/lib/python3.13
# COPY --from=backend-builder /usr/local/bin /usr/local/bin
COPY --from=backend-builder /app/.venv /app/.venv

# 复制后端代码
COPY . /app

# 设置环境变量
#ENV PYTHONPATH=/app
#ENV FLASK_APP=ruoyi_admin/app.py
#ENV FLASK_ENV=production

# 暴露端口
EXPOSE 9000

# 运行脚本迁移，再启动应用
# CMD [".venv/bin/python", "ruoyi_admin/app.py"]
CMD ["/bin/sh", "-c", ".venv/bin/alembic upgrade head && .venv/bin/python ruoyi_admin/app.py"]
