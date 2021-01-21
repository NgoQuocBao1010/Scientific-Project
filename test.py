from datetime import datetime

now = datetime.now()
# now = now.strftime("%Y-%m-%d %H:%M:%S%f")
now = str(now)
print(now)
now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S.%f')
print(type(now))