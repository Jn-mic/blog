import os

from dotenv import load_dotenv as ld

ld()


class Config:
    debug = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SENDGRID_API_KEY=os.environ.get('SENDGRID_API_KEY')
    DEFAULT_SENDGRID_SENDER =  os.environ.get('DEFAULT_SENDGRID_SENDER')

    #  email configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
