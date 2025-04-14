FROM python:3.12-slim-bullseye

# 暴露端口
EXPOSE 8000

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装系统依赖
COPY requirements.txt /app/requirements.txt

# 换源并安装系统依赖
RUN sed -i "s@http://deb.debian.org@http://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1 \
        libgomp1 \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 换源并安装 Python 依赖
RUN python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip && \
    pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip3 install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . /app

# 启动命令 workers 根据自己的机器调整
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--workers", "9", "--log-config", "./log_conf.yaml"]