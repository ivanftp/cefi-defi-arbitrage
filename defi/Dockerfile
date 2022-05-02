# syntax=docker/dockerfile:1
FROM python:3.8
WORKDIR /cefi-defi-arbitrage/defi
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 3001
COPY . .
CMD ["python", "./app.py"]