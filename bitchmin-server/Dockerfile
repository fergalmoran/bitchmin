FROM python:3.8-alpine

RUN apk add --update alpine-sdk

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

ENV DNS_PORT 53
ENV WORKER_PORT 54

EXPOSE 53
EXPOSE 54

CMD [ "python", "./server.py" ]
