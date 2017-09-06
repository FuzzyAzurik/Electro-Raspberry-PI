#!/usr/bin/env python

import Queue
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s', )

queue = Queue.Queue()


def put(item):
    logging.debug("Putting Item into queue %s" % (item))
    queue.put(item)


def get():
    item = queue.get()
    logging.debug("retrieving Item from the queue %s" % (item))
    return item
