FROM python:alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.2.2
ENV POETRY_HOME="/opt/poetry"
ENV PATH=${POETRY_HOME}/bin:$PATH

RUN apk update \
    && apk add curl gcc python3-dev musl-dev openssl-dev libffi-dev

RUN curl -sSL https://install.python-poetry.org | python -

WORKDIR /usr/src/app

COPY pyproject.toml poetry.lock /usr/src/app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY src/ .

CMD poetry run task server

EXPOSE 11801
