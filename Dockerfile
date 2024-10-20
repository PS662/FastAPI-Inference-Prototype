FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE ${FAST_API_PORT}

CMD ["sh", "-c", "uvicorn app.main:app --host ${FAST_API_HOST} --port ${FAST_API_PORT} --reload"]
