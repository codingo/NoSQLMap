FROM python:2.7-alpine

RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/main' >> /etc/apk/repositories
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/community' >> /etc/apk/repositories
RUN apk update && apk add mongodb git

RUN git clone https://github.com/codingo/NoSQLMap.git /root/NoSqlMap

WORKDIR /root/NoSqlMap

RUN python setup.py install

RUN pip2 uninstall certifi -y
RUN pip2 install certifi==2018.10.15

COPY entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/entrypoint.sh

ENTRYPOINT ["/tmp/entrypoint.sh"]
