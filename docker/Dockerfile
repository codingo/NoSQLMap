FROM ubuntu:latest

RUN apt-get update && apt-get install -y python python-pip git mongodb

RUN git clone https://github.com/codingo/NoSQLMap.git /root/NoSqlMap

WORKDIR /root/NoSqlMap

RUN python setup.py install

COPY entrypoint.sh /tmp/entrypoint.sh

RUN chmod +x /tmp/entrypoint.sh

ENTRYPOINT ["/tmp/entrypoint.sh"]
