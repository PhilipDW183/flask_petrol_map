import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        """Base configuration variables"""
        self.SECRET_KEY = os.environ.get("SECRET_KEY") or "Test key"
        if not self.SECRET_KEY:
            raise("Secret key is missing. Something is wrong")
        self.BING_API_KEY = os.environ.get("BING_API_KEY")