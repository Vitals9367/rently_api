FROM python:3.9-buster
WORKDIR /rently_api

ENV PORT=8000

RUN apt-get update && \
    apt-get install -y uwsgi uwsgi-plugin-python3

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV STATIC_ROOT /srv/rently_api/static
RUN mkdir -p $STATIC_ROOT
RUN python manage.py collectstatic

RUN chmod +x docker-entrypoint.sh
EXPOSE ${PORT}

ENTRYPOINT ["./docker-entrypoint.sh"]