FROM jfloff/alpine-python:3.7-onbuild

# FROM alpine:3.11

# copy crontabs for root user
COPY cronjobs/ /etc/crontabs

WORKDIR /usr/src/app
COPY tasks/ /usr/src/app

# start crond with log level 8 in foreground, output to stderr
CMD ["crond", "-f", "-d", "8"]