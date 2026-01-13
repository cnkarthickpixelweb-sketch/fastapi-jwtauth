import os
from dotenv import load_dotenv
import sys

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("USER_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB = os.getenv("DB")


JWT_SECRECT_KEY = os.getenv("JWT_SECRECT_KEY")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 10

# if not JWT_SECRECT_KEY:
#     print("ERROR: JWT_SECRECT_KEY is not set in environment variables")
    # sys.exit(1)

