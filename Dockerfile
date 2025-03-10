FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app

# CMD ["python3", "-m", "main:app"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002", "--reload", "--env-file", ".env"]
