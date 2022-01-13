FROM python:3.9.6

ENV PYTHONUNBUFFERED 1
COPY pip.conf /root/.pip/pip.conf

RUN mkdir -p /home/DjangoApi/App

WORKDIR /home/DjangoApi/App

ADD . /home/DjangoApi/App

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

