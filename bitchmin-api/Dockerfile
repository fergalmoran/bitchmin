FROM python:3.7.4-alpine

RUN adduser -D bitchmin
RUN mkdir /bitchmin
WORKDIR /bitchmin
COPY ./requirements.txt requirements.txt


RUN apk update && \
    apk add --no-cache --virtual build-deps gcc python3-dev musl-dev bind-tools && \
    apk add postgresql-dev && \
    pip install -r requirements.txt


RUN python3.7 -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY server.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP server.py

RUN chown -R bitchmin:bitchmin ./
USER bitchmin

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]