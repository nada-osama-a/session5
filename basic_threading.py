import time

def count1():
    for i in range(1, 10):
        print(f"Task 1: {i}")
        time.sleep(0.5)

def count2():
    for i in range(20, 30):
        print(f" Task 2: {i}")
        time.sleep(0.5)

count1()
count2()    
########################################
import threading
import time

def count_small():
    for i in range(1, 10):
        print(f"Task 1: {i}")
        time.sleep(0.5)

def count_big():
    for i in range(20, 30):
        print(f"\t\tTask 2: {i}")
        time.sleep(0.5)

t1 = threading.Thread(target=count_small)
t2 = threading.Thread(target=count_big)

t1.start()
t2.start()

#############################
import threading
import time

def count_small():
    for i in range(1, 10):
        print(f"Task 1: {i}")
        time.sleep(0.5)

def count_big_daemon():
    i = 20
   
    while True:
        print(f"\t\tTask 2 (Daemon): {i}")
        i += 1
        time.sleep(0.5)



t1 = threading.Thread(target=count_small)              # Non-Daemon 
t2 = threading.Thread(target=count_big_daemon, daemon=True) # Daemon

t1.start()
t2.start()

