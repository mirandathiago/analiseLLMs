import psycopg
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

def connect_database():
    try:
        conn = psycopg.connect(
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            user=os.getenv("USER"),
            password=os.getenv("PASS"),
            dbname=os.getenv("DATABASE")
        )
        return conn
    except psycopg.Error as e:
        print("Erro na conexão com o banco de dados:", e)
