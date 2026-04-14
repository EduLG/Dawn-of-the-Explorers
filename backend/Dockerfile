FROM python:3.12-slim

WORKDIR /app

RUN pip install flask flask-cors flask-jwt-extended flask-sqlalchemy psycopg2-binary python-dotenv

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
