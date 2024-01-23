# Python
import uuid
import datetime

def upload(instance, filename):
    today = datetime.datetime.now()
    file_format = filename.split('.')[-1]
    return f"{today.year}/{today.month}/{today.day}/{uuid.uuid4()}.{file_format}"
