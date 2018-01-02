import threading
import queue
import time

# x = ""
# q = queue.Queue()

# def p():
# 	print("running")

# def loop(q,p):
# 	while q.empty():
# 		time.sleep(1)
# 		print(q.queue)
	
# 	print("passed")
# 	q.get()
# 	t1 = threading.Timer(1,p)
# 	t1.daemon = False
# 	t1.start()



# t = threading.Thread(target=loop,args=(q,p))
# t.start()

# while(x!="Quit"):
# 	x = input("Enter Quit to quit.")
# 	q.put(x)
# 	print(q.queue)
# def p():
# 	print("run")
# t = threading.Timer(1,p)
# t.start()
# time.sleep(5)

# def printit():
# 	threading.Timer(1,printit).start()
# 	print("running!")

# printit()

# print("1")
# time.sleep(-1)
# print("2")

q = queue.Queue()
q.put("something")
q.put("something else")
print(q.get())
print(threading.currentThread().getName())
