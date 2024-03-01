from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getcwd, getenv
from dotenv import load_dotenv

from views import *

load_dotenv()

cwd = getcwd()

app = Flask(__name__)
app.url_map.strict_slashes = False

app.config["SECRET_KEY"] = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{cwd}/{getenv('DB')}.db"

db = SQLAlchemy(app)


if __name__ == "__main__":
    app.run()
