
FROM python:3.6.6-alpine3.6

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apk update && apk add build-base && apk add g++ libressl-dev postgresql-dev libffi-dev gcc musl-dev python3-dev
RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY . .

CMD [ "python", "./main.py" ]