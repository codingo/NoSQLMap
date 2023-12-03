FROM python:2.7-alpine

RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/main' >> /etc/apk/repositories
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/community' >> /etc/apk/repositories
RUN apk update && apk add mongodb git

RUN git clone https://github.com/codingo/NoSQLMap.git /root/NoSqlMap

WORKDIR /root/NoSqlMap

RUN python setup.py install

RUN python -m pip install requests 'certifi<=2020.4.5.1'

COPY entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/entrypoint.sh

ENTRYPOINT ["/tmp/entrypoint.sh"]
