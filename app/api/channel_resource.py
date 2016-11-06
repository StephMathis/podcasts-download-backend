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

from ..models.channel import Channel
from ..lib.tools import id2text, text2id

class ChannelResource(Resource):

    channel_id = fields.CharField(attribute='id', default=None)
    podcasts = fields.ListField(attribute='podcasts', default=None)
    
    class Meta :
        resource_name = 'channels'
        include_resource_uri = False
        
    def obj_get(self, bundle, **kwargs):
        channel_id = kwargs.get('channel_id')
        channel = None
        if Channel.exists(channel_id) :
            channel = Channel(channel_id)
        return channel

    def obj_get_list(self, bundle, **kwargs):
        return Channel.get_channels()

    def patch_detail(self, bundle, **kwargs):
        print("patch_detail",bundle,kwargs)
        channel_id = kwargs.get('channel_id')
        podcast_id = kwargs.get('podcast_id')
        channel = None
        if Channel.exists(channel_id) :
            channel = Channel(channel_id)
            channel.add_podcast(podcast_id)
        else :
            raise NotFound("Channel object not found")
        return channel

    def obj_create(self, bundle, **kwargs):
        title = bundle.data.get('title',None)
        print("obj_create",bundle,kwargs,title)
        if title == None :
            print("obj_create channel_id is None")
            return bundle
        channel_id = Channel.title2id(title)
        if Channel.exists(channel_id) :
            # already exists
            print("obj_create : already exists")
        else :
            # create resource
            print("obj_create : create resource")
            channel = Channel(channel_id)
            bundle.obj = channel
        return bundle


