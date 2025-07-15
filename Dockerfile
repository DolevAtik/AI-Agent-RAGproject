FROM python:3.9-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y --no-install-recommends libsqlite3-dev gcc python3-dev && rm -rf /var/lib/apt/lists/* && apt-get clean
RUN pip install pysqlite3-binary
COPY . .
RUN echo "DEBUG:(2025-06-21 13:10)"
EXPOSE 5000
CMD ["python", "-m", "app.main"]