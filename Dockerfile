FROM python:3.9

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN pip install "poetry==1.1.4"
COPY poetry.lock pyproject.toml /usr/src/app/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

ADD src /usr/src/app/src

EXPOSE 8080

CMD gunicorn  --chdir src "sprint_webserver:create_app"  --config=src/sprint_webserver/gunicorn_config.py --worker-class aiohttp.GunicornWebWorker
