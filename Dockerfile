# 使用官方 Python 3.10.9 镜像作为基础镜像
FROM python:3.10.9

# 在容器内创建并切换到工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY ./src /app/src
COPY ./requirement.txt /app/requirement.txt

# 安装虚拟环境工具
RUN pip install virtualenv

# 创建并激活虚拟环境
RUN python -m venv venv
RUN . venv/bin/activate

# 安装项目依赖项
RUN pip install -r requirement.txt

# 定义容器启动命令，运行您的 Python 项目
CMD ["python", "src/get_douban.py"]
