# -*- coding: utf-8 -*-
import os

from dotenv import load_dotenv,find_dotenv
from os import getenv
# loaddotenv()
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
#auth0 env
AUTH0_DOMAIN = getenv("AUTH0_DOMAIN")
ALGORITHMS = ['RS256']
API_AUDIENCE = getenv("API_IDENTIFIER")

