FROM python:3.9.13-slim
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

WORKDIR /app

COPY app .

ENTRYPOINT [ "python", "main.py" ]