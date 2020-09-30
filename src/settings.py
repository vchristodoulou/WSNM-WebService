import os

from dotenv import load_dotenv


load_dotenv()

APP_SETTINGS = os.getenv("APP_SETTINGS")
SERVER_IP = os.getenv("SERVER_IP")
SERVER_PORT = os.getenv("SERVER_PORT")
