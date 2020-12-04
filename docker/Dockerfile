FROM docker.io/python:3.8-alpine AS base
MAINTAINER  Oz Tiram <oz.tiram@gmail.com>

RUN apk update && \
    apk add g++ libffi-dev git openssl-dev && \
    pip3 install --upgrade pip && \
    pip3 install pipenv

ENV \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100
#
#
WORKDIR /run/app
#
#
ADD requirements.txt /run/app/
RUN python -m venv venv
RUN /run/app/venv/bin/pip install -r /run/app/requirements.txt
RUN /run/app/venv/bin/pip install uwsgi
#
FROM python:3.8-alpine as smallimage
COPY --from=base /run/app /run/app

RUN apk update && apk add sqlite mailcap
#
WORKDIR /run/app
#
RUN deluser xfs # remove uid 33 which is www-data in debian
RUN adduser -D app --uid 33 && \
	test -d /var/lib/app/db || mkdir -pv /var/lib/app/db && \
	chown -vR app:app /var/lib/app/

ADD docker/entrypoint.sh /usr/bin/
ADD app.py /run/app/
ADD bottle_peewee.py /run/app/

# Note: SQLite requires this directory to be writeable by uid 33
VOLUME ["/var/lib/app/db"]
#
EXPOSE 9001
USER app
#
CMD ["/usr/bin/entrypoint.sh"]
