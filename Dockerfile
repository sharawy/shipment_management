FROM python:3.8.12

RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get install -y poppler-utils && \
    apt-get install binutils libproj-dev gdal-bin -y && \
    apt-get install wkhtmltopdf -y && \
    apt-get install gettext -y

COPY . /app

WORKDIR /app

RUN pip install virtualenv && virtualenv /venv && . /venv/bin/activate &&\
    pip install poetry && \
    poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

ENTRYPOINT ["/entrypoint.sh"]

LABEL application="shipment-management"