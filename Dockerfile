FROM python:3.10

ARG DATABASE_URL
ARG DATABASE_NAME
ARG SECRET_KEY

ENV DATABASE_URL=$DATABASE_URL
ENV DATABASE_NAME=$DATABASE_NAME
ENV SECRET_KEY=$SECRET_KEY

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]