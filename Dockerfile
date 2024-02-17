FROM python:3.11-slim

WORKDIR /usr/src/app

COPY parameters.py .
COPY watermark.py .
COPY requirements.txt .
COPY Roboto/ Roboto/
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "watermark.py"]