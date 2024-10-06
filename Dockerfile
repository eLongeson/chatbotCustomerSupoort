FROM python:3.9-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


RUN mkdir -p /app/persist && chmod 777 /app/persist
RUN mkdir -p /app/data && chmod 777 /app/data

COPY .env .env

#stage 2
FROM python:3.9-slim

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app /app

RUN chmod -R 777 /app/persist && chmod -R 777 app/data

EXPOSE 6000

CMD [ "python", "app.py" ]