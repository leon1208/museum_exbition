#/bin/sh

## 编译
docker-compose -f docker/docker-compose.yaml build

## 编译加启动
docker-compose -f docker/docker-compose.yaml up -d --build

#docker build --target frontend-nginx -t museum_exhibition_web:0.0.1 -f docker/Dockerfile .
#docker build --target backend-runtime -t museum_exhibition_app:0.0.1 -f docker/Dockerfile .
