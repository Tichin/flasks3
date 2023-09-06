import os
import logging
import boto3
from botocore.exceptions import ClientError
# import uuid

from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy

from models import db, connect_db, File

app = Flask(__name__)

BUCKET = os.environ['MY_BUCKET']

BUCKET_BASE_URL = f"https://{BUCKET}.s3.us-west-1.amazonaws.com/photos/"

# app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///flasks3")

connect_db(app)


@app.get("/")
def home():
    """test home"""
    def upload_file(file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

    # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

    # Upload the file
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
            print("RESPONSE: ", response)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    s3 = boto3.client('s3')
    # with open("testupload.txt", "rb") as f:
    #     print("F: ", f)
    #     s3.upload_fileobj(f, "flasks3-test", "files/")

    s3.upload_file("kitten.jpeg", f'{BUCKET}', "photos/kitten")

    # BUCKET_BASE_URL + {file_name}
    newFile = File(image_url=f'{BUCKET_BASE_URL}kitten')

    db.session.add(newFile)
    db.session.commit()

    return render_template("index.html")
