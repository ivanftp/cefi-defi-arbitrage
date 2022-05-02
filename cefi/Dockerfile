# syntax=docker/dockerfile:1
FROM python:3.8
WORKDIR /cefi-defi-arbitrage/cefi
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 3000
COPY . .
CMD ["python", "./app.py"]