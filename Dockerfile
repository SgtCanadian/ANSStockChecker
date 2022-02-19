FROM python:3.10-alpine

ENV CONFIG_PATH /config
ENV CHECK_URL _
ENV NOTIFY_MESSAGE "In Stock"
ENV REFRESH_SEC 300
ENV TELEGRAM_TOKEN _
ENV TELEGRAM_CHATID _

RUN mkdir /config

WORKDIR /app
COPY requirements.txt .
COPY main.py .

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]