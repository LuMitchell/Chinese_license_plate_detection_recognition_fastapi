# Docker 快速安装 FastAPI 版的车牌识别

本项目提供了一个基于 FastAPI 的车牌识别服务，并通过 Docker 实现快速部署。以下是安装和启动服务的详细步骤。

## 步骤

### 1. 安装 Docker 和 Docker Compose
在开始之前，请确保你的系统已安装 Docker 和 Docker Compose 。如果尚未安装，可参考以下官方指南：
- [Docker 安装指南](https://docs.docker.com/get-docker/)
- [Docker Compose 安装指南](https://docs.docker.com/compose/install/)

### 2. 下载项目代码
通过 Git 将项目代码克隆到本地：
```bash
git clone https://github.com/LuMitchell/Chinese_license_plate_detection_recognition_fastapi.git
```

### 3. 制作 Docker 镜像
进入项目目录并构建 Docker 镜像：
```bash
cd Chinese_license_plate_detection_recognition_fastapi

docker build -t plate_ocr:fastapi-1.0 --network host .
```
注意：构建过程可能需要一些时间，请耐心等待。

### 4. 启动服务
使用 Docker Compose 启动服务：
```bash
docker-compose up -d
```
服务启动后，你可以通过以下地址访问 API 文档：

- 本地运行：http://127.0.0.1:8000/docs
- 或使用你的机器IP地址，例如：http://<你的IP>:8000/docs

## References
本项目 Fork 自 [Chinese_license_plate_detection_recognition](https://github.com/we0091234/Chinese_license_plate_detection_recognition)
