import os
os.system('apt update')
os.system('apt install python3-pip -y')
os.system('apt-get install libpq-dev python-dev poppler-utils -y')
os.system('pip3 install pandas sqlalchemy==1.3.24 numpy flask==1.1.2 flask-cors flask-restplus psycopg2 python-dotenv gunicorn tabulate pdf2image pillow requests pyjwt')
os.system('pip3 uninstall --yes Werkzeug')
os.system('pip3 install Werkzeug==0.16.1')