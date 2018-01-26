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

from ..models.channel import Channel, FileChannelStore
from ..lib.tools import id2text, text2id

class ChannelPodcastResource(Resource):

    channel_id = fields.CharField(attribute='id', default=None)
    podcasts = fields.ListField(attribute='podcasts', default=None)
    
    class Meta :
        resource_name = 'channels'
        include_resource_uri = False
        
    def obj_create(self, bundle, **kwargs):
        channel_id = kwargs.get('channel_id')
        #podcast_id = kwargs.get('podcast_id')
        podcast_url = bundle.data.get("podcast_url")
        podcast_id = text2id(podcast_url)
        #print("ChannelPodcastResource.obj_create",channel_id,podcast_url,podcast_id)
        channel = None
        if Channel.exists(channel_id) :
            channel = Channel(channel_id)
            channel.add_podcast(podcast_id)
            bundle.obj = channel
        return bundle
       
    def obj_delete(self, bundle, **kwargs) :
        print("ChannelPodcastResource : obj_delete")
        channel_id = kwargs.get('channel_id')
        podcast_id = kwargs.get('podcast_id')
        print("ChannelPodcastResource :", channel_id, podcast_id)
        channel = None
        channel_store = FileChannelStore()
        if channel_store.exists(channel_id) :
            channel = channel_store.get_channel(channel_id)
            channel.remove_podcast(podcast_id)
            channel_store.save_channel(channel)
            bundle.obj = channel
        return bundle



