import time
from threading import Thread ,Lock ,RLock

lock = RLock()

def person(name):
    with lock:
        print(f"Name: {name}")

def count1():
    for i in range(1, 10):
        with lock: 
            print(f"Task 1: {i}")
            person("ahmed")
        time.sleep(0.5)

def count2():
    for i in range(21, 40):  
        with lock:
            print(f"\t\tTask 2: {i}")
        time.sleep(0.5)


t1=Thread(target=count1)
t2=Thread(target=count2, daemon=True)

t1.start()
t2.start()


t=Thread(target=person,args=("nada",))



