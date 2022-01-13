FROM python:3.9.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /home/DockerDemo
ADD . /home/DockerDemo
WORKDIR /home/DockerDemo
RUN  pip3 install -r ./project/App/requirements.txt -i https://pypi.douban.com/simple
RUN  pip3 install uwsgi