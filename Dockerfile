FROM python:3.10-slim

WORKDIR /app
COPY requirements* .
RUN pip install -r requirements.txt
COPY src/* ./
ENTRYPOINT [ "python", "telegram-dtlkfb-bot.py" ]
