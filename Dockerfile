FROM python:3.10-slim

WORKDIR /app
COPY ./app /app
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

EXPOSE 8000
CMD ["python", "main.py"]
