from dotenv import load_dotenv
import os

load_dotenv()
credentials = {
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'database': os.getenv('DATABASE'),
    'host': os.getenv('HOST'),
    'secret_key': os.getenv('SECRET_KEY')
}