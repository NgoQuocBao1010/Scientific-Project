from datetime import datetime

lastimeCheck = datetime.now()

secondToCheck = (datetime.now() - lastimeCheck).timestamp()
print(secondToCheck)
secondRun = 0
# while True:
#     secondRun = datetime.now().second - lastimeCheck.second
#     print(secondRun)

#     if secondRun > secondToCheck:
#         break
