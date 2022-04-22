import threading

'''
Queue with semaphores for producer-consumer
'''
class Queue:
    def __init__(self):
        self.queue = []                       # the queue ...
        self.qlock = threading.Lock()         # lock object. initially unlocked.
        self.full = threading.Semaphore(0)    # initially all slots empty
        self.empty = threading.Semaphore(10)  # There are 10 total empty slots

    def enqueue(self, val):
        self.empty.acquire()                  # acquire a Semaphore. decrement atomic counter
        self.qlock.acquire()                  # acquire a lock (changes state to locked)
        self.queue.append(val)                # add item to queue
        self.qlock.release()                  # releases lock
        self.full.release()                   # release Semaphore. increment atomic counter
        
    def dequeue(self):
        self.full.acquire()                   # acquire a Semaphore. decrement atomic counter.
        self.qlock.acquire()                  # acquire a lock (changes state to locked)
        val = self.queue.pop(0)               # get the next item in the queue
        self.qlock.release()                  # releases lock
        self.empty.release()                  # release Semaphore. increment atomic counter.
        return val                            # return the next queue item

    
