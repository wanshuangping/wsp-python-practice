# 1. 使用官方 Python 轻量版基础镜像
FROM python:3.9-slim

# 2. 设置容器内的工作目录
WORKDIR /app

# 3. 将本地的所有文件复制到容器的 /app 目录下
COPY . .

# 4. 安装之前生成的 requirements.txt 里的依赖
RUN pip install --no-cache-dir -r requirements.txt

# 5. 暴露 Streamlit 默认的 8501 端口
EXPOSE 8501

# 6. 启动命令
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]