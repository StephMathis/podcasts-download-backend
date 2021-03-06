# -*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

import base64
import random

import gevent

from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpNotFound
from tastypie.resources import Resource

from django.conf.urls import url
from django.http import StreamingHttpResponse

from .wish.wish_resource import WishResource
from ..lib.resources.default_meta_mixin import DefaultMetaMixin
from ..lib.resources.url_helper import UrlHelper

from ..models.trackergroup import TrackerGroup

class TrackerGroupResource(Resource):

    tracker_group_id = fields.CharField(attribute='id', default=None)
    items_status = fields.ListField(attribute='items_status', default=None)
    
    class Meta :
        resource_name = 'trackergroups'
        include_resource_uri = False
        
    def obj_get(self, bundle, **kwargs):
        tracker_group_id = kwargs.get('tracker_group_id')
        tracker_group = TrackerGroup(tracker_group_id)
        tracker_group.get_items_status()
        return tracker_group

