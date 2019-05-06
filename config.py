import os
from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))

API_key = os.environ.get('API_KEY')

class Config():

	SECRET_KEY = os.environ.get('SECRET_KEY') or 'han-shot-first'
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)

