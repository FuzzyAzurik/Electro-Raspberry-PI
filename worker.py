#!/usr/bin/env python

from threading import Thread
from service.service import RestService
import queue
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s', )


class Worker(Thread):
    meterId = "99806"
    applicationName = "electro-backend"
    endpoint = "http://jacobwortmann.dk:9080/%s/api/meter/%s/readings/" % (applicationName, meterId)
    user = "jacob"
    password = "secret"

    restService = None
    """docstring for Worker"""

    def __init__(self, name):
        super(Worker, self).__init__(name=name)
        self.restService = RestService(self.endpoint, self.user, self.password)

    def run(self):
        while True:
            item = queue.get()
            if item is not None:
                try:
                    wasSuccessful = self.restService.post(item)
                    if not wasSuccessful:
                        logging.error("Unable to post to endpoint, putting reading back to queue")
                        queue.put(item)
                except Exception as e:
                    logging.error("Unable to post to endpoint, putting reading back to queue")
                    queue.put(item)
