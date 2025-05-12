FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Do not change the port a proxy is listening on the different port and redirecting
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]