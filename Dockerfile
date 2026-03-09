# 使用基于 Debian 12 (bookworm) 的 Python 3.12 官方镜像，这对安装 Playwright 的系统依赖最友好
FROM python:3.12-bookworm

# 设置工作目录
WORKDIR /app

# 将当前目录的所有文件复制到容器的工作目录中
COPY . /app/

# 升级 pip，并通过 pyproject.toml 安装所有项目依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# 安装 Playwright 所需的浏览器内核及系统依赖 (体积较大，需要一些时间下载)，如果在Docker外部就获取了REFRESH_TOKEN可以不装，直接注释掉
RUN playwright install --with-deps chromium

# 暴露给同网络其他容器的端口
EXPOSE 8080