#! /bin/bash
nginx
gunicorn -w 4 -b 0.0.0.0:5000 --timeout=300 wsgi:app
