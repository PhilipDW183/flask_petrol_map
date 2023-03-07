import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        """Base configuration variables"""
        self.SECRET_KEY = os.environ.get("SECRET_KEY")
        if not self.SECRET_KEY:
            raise("Secret key is missing. Something is wrong")