from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="postgres"
DB_USER="postgres"
DB_PASS="112643"

DB_HOST_TEST="localhost"
DB_PORT_TEST="5432"
DB_NAME_TEST="postgres"
DB_USER_TEST="postgres"
DB_PASS_TEST="112643"

SECRET_AUTH = os.environ.get("SECRET_AUTH")