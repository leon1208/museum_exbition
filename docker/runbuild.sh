#/bin/sh

## 编译,在项目根目录下执行
APP_VERSION=$(cat VERSION) docker-compose -f docker/docker-compose.yaml build

## 编译加启动,在项目根目录下执行
APP_VERSION=$(cat VERSION) docker-compose -f docker/docker-compose.yaml up -d --build

#docker build --target frontend-nginx -t museum_exhibition_web:0.0.1 -f docker/Dockerfile .
#docker build --target backend-runtime -t museum_exhibition_app:0.0.1 -f docker/Dockerfile .
