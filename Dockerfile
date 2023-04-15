FROM python:3.9-buster
WORKDIR /rently_api

ENV PORT=8000

RUN apt-get update && \
    apt-get install -y uwsgi uwsgi-plugin-python3

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE ${PORT}

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]