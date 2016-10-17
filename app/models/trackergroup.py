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

def waiting_until_closed(key, closeable) :
    while closeable.closed == False:
        time.sleep(1)
        print('myfunction',time.ctime(time.time()))
    print("finished !!")
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    mc.set(key, "Finished")

class TrackerGroup(ModelMixin):
    def __init__(self, id) :
        self.id = id
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        if mc.get(self.id) == None :
            mc.set(self.id,[])

    def _get_item_key(self, item_id) :
        return "%s-%s" % (self.id,item_id)
        
    def add_closeable(self, item_id, closeable) :
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        items = mc.get(self.id)
        items.append(item_id)
        mc.set(self.id,items)
        key = self._get_item_key(item_id)
        mc.set(key , "Pending")
        _thread.start_new_thread( waiting_until_closed, (key, closeable,) )

    def get_items_status(self) :
        items_status = []
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        item_ids = mc.get(self.id)
        for item_id in item_ids :
            key = self._get_item_key(item_id)
            item_status = mc.get(key)
            items_status.append({"id":item_id,"status":item_status})
        self.items_status = items_status
        return self.items_status

