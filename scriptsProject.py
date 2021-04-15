import os
import socket

HOSTNAME = socket.gethostname()
IP_ADDRESS = socket.gethostbyname(HOSTNAME)
os.system(f'powershell "cd src; python manage.py runserver {IP_ADDRESS}:8000"')
os.system(f'powershell "python manage.py checkDis.py')
print("Chao")
