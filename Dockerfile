FROM python:3.14.7-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY asgi.py application.properties ./
COPY src/ src/
COPY static/ static/
COPY templates/ templates/
COPY assets/ assets/

EXPOSE 8000

CMD ["python", "asgi.py"]
