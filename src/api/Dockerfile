FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ADD ./ /app

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "/app/cert/privkey.pem", "--ssl-certfile", "/app/cert/cert.pem"]

