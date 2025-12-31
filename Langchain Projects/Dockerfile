FROM python:3.10-slim

WORKDIR /simple_genapp/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY simple_genapp/app.py .

CMD ["python", "app.py"]
