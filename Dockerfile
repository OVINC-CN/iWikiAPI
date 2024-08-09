FROM python:3.10
RUN mkdir -p /usr/src/app/logs
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip3 install -U pip && pip3 install -r requirements.txt
