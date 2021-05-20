import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
# print(load_dotenv())  # True

# # Or, explicitly provide path to '.env'
# from pathlib import Path

# env_path = Path(".") / ".env"
# load_dotenv(dotenv_path=env_path)

AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")
