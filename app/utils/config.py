import os
from dotenv import load_dotenv

load_dotenv()


DB_URL :str   = os.getenv('MONGODB_URI')
DB_NAME : str = os.getenv('MONGODB_NAME')
