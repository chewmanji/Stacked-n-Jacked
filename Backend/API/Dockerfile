FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src
COPY ./alembic /code/alembic
COPY ./alembic.ini /code/alembic.ini

CMD ["fastapi", "run", "src/main.py", "--port", "80"]