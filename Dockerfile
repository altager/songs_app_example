FROM python:3.7.2-slim

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

ADD requirements.txt .
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get purge -y --auto-remove gcc

COPY . /app
RUN python setup.py install

# TODO: move host and port to env var
EXPOSE 8080
ENTRYPOINT ["./entrypoint.sh"]
