FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas matplotlib sqlalchemy psycopg2

WORKDIR /app
COPY . . 

ENTRYPOINT [ "python", "main.py" ]