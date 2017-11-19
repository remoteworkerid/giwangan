FROM python:2.7-alpine
MAINTAINER Eko Wibowo <swdev.bali@gmail.com>

ENV INSTALL_PATH /web_app
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .