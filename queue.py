
from Queue import Queue
import logging

logging.basicConfig(level=logging.DEBUG,format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

queue = Queue()

def put(item):
    logging.debug("Putting Item into queue %s" %(item))
    queue.put(item)

def get():
    return queue.get()        