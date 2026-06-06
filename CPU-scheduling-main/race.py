import threading

balance = 1000
lock = threading.Lock()

def withdraw(amount):
    global balance

    with lock:
        if balance >= amount:
            balance -= amount
            print(f"Withdrawn {amount}, Balance = {balance}")

t1 = threading.Thread(target=withdraw, args=(700,))
t2 = threading.Thread(target=withdraw, args=(500,))

t1.start()
t2.start()

t1.join()
t2.join()

print("Final Balance:", balance)