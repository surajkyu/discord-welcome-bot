# imports

import os
from pathlib import Path
from src.index import client
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

token = os.getenv("TOKEN") # fetch token from .env
client_id = os.getenv("CLIENT_ID") # fetch client id from .env - For future reference

if token is None: # token error handling
    raise RuntimeError("TOKEN was not found in .env")

client.run(token) # run bot
