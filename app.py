import os
import boto3
# import uuid

from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy

from models import db, connect_db, File


app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///flasks3")

connect_db(app)


@app.get("/")
def home():
    """test home"""

    return render_template("index.html")
