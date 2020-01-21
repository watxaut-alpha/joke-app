import os

# API vars
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM")
DOCS_USER: str = os.getenv("DOCS_USER")
DOCS_PASSWORD: str = os.getenv("DOCS_PASSWORD")

# DB vars
POSTGRES_USER: str = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")

DB_HOST: str = os.getenv("DB_HOST")
SCHEMA_NAME: str = os.getenv("SCHEMA_NAME")

# MailGun
MAILGUN_USER: str = os.getenv("MAILGUN_USER")
MAILGUN_PWD: str = os.getenv("MAILGUN_PWD")
