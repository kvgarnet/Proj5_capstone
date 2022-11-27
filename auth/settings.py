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
#test db env
DB_NAME = getenv("DATABASE_NAME")
TEST_DB_NAME = getenv("TEST_DATABASE_NAME")
DB_USER=getenv("DATABASE_USER")
DB_PASSWORD = getenv("DATABASE_PASS")
