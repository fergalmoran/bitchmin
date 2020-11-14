FROM python:3.7

COPY ./requirements.txt /requirements.txt
RUN apt update && \
    apt install -y libblas-dev && \
    pip install gunicorn

RUN pip install -r requirements.txt

COPY app /app
COPY migrations /migrations
COPY server.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_ENV production
ENV FLASK_APP server.py

#RUN chown -R bitchmin:bitchmin ./
#USER bitchmin

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]