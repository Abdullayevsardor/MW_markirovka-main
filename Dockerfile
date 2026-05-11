FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p /app/static/category && chmod -R 777 /app/static

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# ... (avvalgi qismlar o'zgarishsiz)
CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
