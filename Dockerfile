FROM python:3.13-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY /app /code/app

EXPOSE 8000

CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0"]