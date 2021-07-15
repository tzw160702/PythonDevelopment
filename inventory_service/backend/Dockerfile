FROM python:3.8

WORKDIR /backend

ADD . /backend

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host pypi.douban.com --upgrade pip && pip3 install -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host pypi.douban.com -r requirements.txt

CMD ["python", "/backend/main.py"]
