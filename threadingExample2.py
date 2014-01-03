import Queue
from random import randint
from time import sleep
import threading
import urllib2

# called by each thread
def print_number(q, number):
   # Sleeps a random 1 to 10 seconds
   sleep(number)
   print str(number)
   q.put(str(number))

theurls = [randint(1,10) for i in xrange(1,10)]
print theurls

q = Queue.Queue()
thread_list = []

for u in theurls:
    t = threading.Thread(target=print_number, args = (q,u))
    thread_list.append(t)

for t in thread_list:
	t.start()

for t in thread_list:
	t.join()

while not q.empty():
    print q.get()