#!/usr/bin/env python

import datetime

class Reading(object):
    reading = 0
    readingRatio = 0.0
    readingTime = ""
    """docstring for Reading"""
    def __init__(self, reading, readingRatio):
        super(Reading, self).__init__()
        self.reading = reading
        self.readingRatio = readingRatio
        self.readingTime  = str(datetime.datetime.now().isoformat())
    
    def __str__(self):
        return "ReadingClass: [reading: %d, readingRatio: %.2f, readingTime: %s]" %(self.reading, self.readingRatio, self.readingTime)

    def toJson(self):
        return '''{
            "lightValue": %d,
            "lightRatio": %.2f,
            "readingTime": "%s",
            "meterId": %d
        }''' %(self.reading, self.readingRatio, self.readingTime, 99806)