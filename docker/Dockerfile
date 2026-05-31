FROM python:3.12-slim

WORKDIR /app

COPY requirements/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY data/ data/
COPY src/ src/

ENV PYTHONPATH=src

EXPOSE 8080

CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080"]
