FROM python:3.10-slim

# Set build-time variable (default: production)
ARG ENV=production

# Set runtime environment variable
ENV ENV=$ENV

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# For dev: uvicorn with --reload
# For prod: uvicorn without --reload
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 $([ \"$ENV\" = \"development\" ] && echo \"--reload\")"]
