FROM python:3.8-slim

WORKDIR /flask-app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENTRYPOINT ["python3", "backend/main.py"]