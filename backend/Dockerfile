FROM python:3.8-slim

WORKDIR /task

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python3 main.py
