import threading
from random import randint
from time import sleep

def printNumber():
   # Sleeps a random 1 to 10 seconds
   number = int(randint(1,10))
   sleep(number)
   print str(number)
   return str(number)

thread_list = []
result = []

for i in range(1,10):
   # Instatiates the thread
   # (i) does not a sequence make, so (i,)
   t = threading.Thread(target=printNumber, args=())
   # Sticks the thread in a list so that it remains accessible 
   thread_list.append(t)

# Starts threads
for thread in thread_list:
   result.append(thread.start())

# This blocks the calling thread until the thread whose join() method is called is terminated.
# From http://docs.python.org/2/library/threading.html#thread-objects
for thread in thread_list:
   thread.join()

# Demonstrates that the main process waited for threads to complete
print "Done"
print result