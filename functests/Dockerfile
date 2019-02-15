FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/functests

COPY ./bin ./bin
COPY ./functests/requirements.txt .
COPY ./entrypoint.sh .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./functests /app/functests

RUN mkdir -p /output
VOLUME ["/output"]

ENTRYPOINT ["./entrypoint.sh"]
