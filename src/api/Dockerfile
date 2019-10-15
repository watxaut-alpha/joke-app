FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./ /app

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5050"]