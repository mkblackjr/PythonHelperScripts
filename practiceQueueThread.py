import threading
import time
import queue

class RunClass():
    def __init__(self):
        print("RunClass initialized.\n")

    def run(self,arg):
        while True:
            print(arg)
            time.sleep(1)

        
class Queue_Thread_Practice():
    _example = RunClass()

    def __init__(self):
        print("Initialized.\n")

    def on_start(self):
        arg = "running"
        self._thread = threading.Thread(name="PracticeThread",target=self._example.run,args=(arg,))
        # self._thread.daemon = True
        print("Thread Daemon = " + str(self._thread.daemon))
        self._thread.start()
        print("Thread Starting")
        time.sleep(1)



# class ThreadingExample(object):
#     """ Threading example class
#     The run() method will be started and it will run in the background
#     until the application exits.
#     """

#     def __init__(self, interval=1):
#         """ Constructor
#         :type interval: int
#         :param interval: Check interval, in seconds
#         """
#         self.interval = interval

#         thread = threading.Thread(target=self.run, args=())
#         thread.daemon = True                            # Daemonize thread
#         thread.start()                                  # Start the execution

#     def run(self):
#         """ Method that runs forever """
#         while True:
#             # Do something
#             print('Doing something imporant in the background')

#             time.sleep(self.interval)


# def get_steps(q):
#     while(True):
#         if(q.qsize()>0):
#             name = threading.currentThread().getName()
#             steps = q.get();
#             print("Executed %s steps.\n" % steps)
#             q.task_done()
 
# def add_steps(q,steps):
#     q.put(steps)
#     print("Put %s into queue.\n" % steps)

# def define_thread():
#     q = queue.Queue(maxsize = 3)
#     t = threading.Thread(name = "ConsumerThread", target=get_steps, args=(q,))
#     t.start()
#     return q

# def main_function():
#     q=define_thread()
#     while True:
#         steps = input("What are steps?\n")
#         q.put(steps)
 
#     q.join()

 
if __name__ == '__main__':
    # main_function()
    q = Queue_Thread_Practice()
    q.on_start()

    # example = ThreadingExample()
    # time.sleep(3)
    # print('Checkpoint')
    # time.sleep(2)
    # print('Bye')

