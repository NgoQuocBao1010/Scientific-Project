import time 

start = time.time()
i = 0

while True:
    end = time.time()
    print(start)
    # print(end - start)
    if round(end - start) == 5:
        print(i)
        start = end
    i += 1
