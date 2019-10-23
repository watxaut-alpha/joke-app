FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./ /app

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--ssl-certfile", "/etc/chain.pem", "--ssl-keyfile", "/etc/cert.pem"]
