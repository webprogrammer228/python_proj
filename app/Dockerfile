FROM python:3.6.8-alpine3.9

ENV GROUP_ID=1000 \
    USER_ID=1000

ENV PYTHONPATH=/var/www

WORKDIR /var/www/

ADD . /var/www/
ADD entrypoint.sh /var/www/entrypoint.sh

RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN pip install pymongo

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

USER www

EXPOSE 5000

CMD ["sh", "/var/www/entrypoint.sh"]