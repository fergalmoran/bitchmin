FROM python:3.8-alpine

COPY ./requirements.txt /requirements.txt

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  && pip install -r requirements.txt \
  && pip install gunicorn \
  && apk del build-deps

COPY app /app
COPY .env /
COPY migrations /migrations
COPY server.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_ENV production
ENV FLASK_APP server.py

#RUN chown -R bitchmin:bitchmin ./
#USER bitchmin

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]