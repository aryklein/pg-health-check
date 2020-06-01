FROM python:3.8-alpine
LABEL maintainer="Ary Kleinerman"
RUN apk update && apk upgrade && \
    apk add --virtual .build-deps --no-cache gcc musl-dev make file libffi-dev postgresql-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir Flask && \
    pip install --no-cache-dir gevent && \
    pip install --no-cache-dir psycopg2
RUN apk del .build-deps && \
    rm -rf /var/cache/apk/* /root/.cache /tmp/*
RUN apk add --no-cache postgresql-libs
COPY pg_healthcheck.py /app/pg_healthcheck.py
WORKDIR /app
EXPOSE 19090
CMD ["python", "pg_healthcheck.py", "-h"]
