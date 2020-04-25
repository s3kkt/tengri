FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade -r requirements.txt

COPY . /app/

CMD ["python3", "/app/tengri.py"]
