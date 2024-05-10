FROM python:3.9

RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY build /app/build
COPY app.py /app
COPY wsgi.py /app
