FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY /app /code/app

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--reload", "app.main:app"]