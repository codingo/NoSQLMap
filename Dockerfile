FROM python:3.12-alpine

RUN cat /etc/*alpine*

RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/main' >> /etc/apk/repositories \
    && echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/community' >> /etc/apk/repositories \
    && apk update && apk add mongodb git

ADD . /code

WORKDIR /code

RUN python -m pip install requests certifi setuptools six \
    && pip install .

ENTRYPOINT ["nosqlmap.py"]
