FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app


COPY . /usr/src/app

RUN pip install -e .[dev] -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir

CMD [ "python","trinity/main.py" ]