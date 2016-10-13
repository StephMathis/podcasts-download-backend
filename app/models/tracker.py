#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#
import base64
import requests
import _thread, time
import memcache

from synthetic import synthesize_constructor
from synthetic import synthesize_property

from .mixins.model_mixin import ModelMixin

# TRACKER_REQUEST = {}


@synthesize_constructor()
@synthesize_property('id', contract='string|None')
#@synthesize_property('status', contract='string|None')

def callback(tracker, closeable) :
    tracker.closeable = closeable
    while tracker.closeable.closed == False:
        time.sleep(1)
        print('myfunction',time.ctime(time.time()))
    print("finished !!")
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    mc.set(tracker.id, "Finished")

class Tracker(ModelMixin):
    def __init__(self, id) :
        self.id = id
        
    def setCloseable(self, closeable) :
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        mc.set(self.id, "Pending")
        _thread.start_new_thread( callback, (self, closeable,) )

    # def _getStatus(self) :
    #     closable = TRACKER_REQUEST.get(self.id, None)
    #     if closable == None :
    #         return "NotStarted"
    #     if closable.closed :
    #         return "Finished"
    #     return "Pending"

    def getStatus(self) :
        self.status = "NotStarted"
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        status = mc.get(self.id)
        if status :
            self.status = status
        return self.status

