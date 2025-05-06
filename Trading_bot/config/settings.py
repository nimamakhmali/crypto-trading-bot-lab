import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    return os.getenv("API_KEY")

def get_api_secret():
    return os.getenv("API_SECRET")