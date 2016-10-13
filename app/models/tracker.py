#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#
import base64
import requests

from synthetic import synthesize_constructor
from synthetic import synthesize_property

from .mixins.model_mixin import ModelMixin

TRACKER_REQUEST = {}


@synthesize_constructor()
@synthesize_property('id', contract='string|None')
#@synthesize_property('status', contract='string|None')

class Tracker(ModelMixin):
    def __init__(self, id) :
        self.id = id
        
    def setCloseable(self, closable) :
        self.closable = closable
        TRACKER_REQUEST[self.id] = self.closable

    def _getStatus(self) :
        closable = TRACKER_REQUEST.get(self.id, None)
        if closable == None :
            return "NotStarted"
        if closable.closed :
            return "Finished"
        return "Pending"

    def getStatus(self) :
        self.status = self._getStatus()
        return self.status

