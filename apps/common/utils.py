# Python
import uuid
import datetime
import os
from io import BytesIO
from PIL import Image, ImageOps
from django.utils import timezone
from django.utils.text import slugify
from django.core.files import File

def upload(instance, filename):
    today = datetime.datetime.now()
    file_format = filename.split('.')[-1]
    return f"{today.year}/{today.month}/{today.day}/{uuid.uuid4()}.{file_format}"


def compress_image(image):
    extension = image.file.name.split(".")[-1].lower()
    if extension not in ["jpg", "png", "jpeg"]:
        raise ValueError("Invalid format")
    im = Image.open(image)
    if im.mode != "RGB":
        im = im.convert("RGB")
    im = ImageOps.exif_transpose(im)
    width, height = im.size
    ratio = min(1080 / width, 1080 / height)
    im = im.resize((int(width * ratio), int(height * ratio)), Image.ANTIALIAS)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=70)
    # create a django-friendly Files object
    new_image = File(im_io, name=image.name)
    return new_image