FROM python:3.8-slim-buster

WORKDIR /app
RUN apt-get update && apt-get install -y tesseract-ocr
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
