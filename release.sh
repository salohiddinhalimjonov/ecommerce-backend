#!/bin/bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
python manage.py migrate
