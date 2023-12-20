from configparser import ConfigParser

config_parser = ConfigParser()
config_parser.read(("CONFIG", "./config_data/config.ini"))
db_username = config_parser.get("DATABASE", "DB_USERNAME")
db_password = config_parser.get("DATABASE", "DB_PASSWORD")
db_host = config_parser.get("DATABASE", "DB_HOST")
db_name = config_parser.get("DATABASE", "DB_NAME")
db_port = config_parser.get("DATABASE", "DB_PORT")
USER_LOGIN_SECRET_KEY=config_parser.get("USERS", "USER_LOGIN_SECRET_KEY")
HOST='0.0.0.0'
PORT='8000'

db_string=f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"