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
from tastypie.http import HttpNotFound, HttpConflict
from tastypie.resources import Resource

from django.conf.urls import url
from django.http import StreamingHttpResponse

from .wish.wish_resource import WishResource
from ..lib.resources.default_meta_mixin import DefaultMetaMixin
from ..lib.resources.url_helper import UrlHelper

from ..models.channel import Channel, FileChannelStore
from ..lib.tools import id2text, text2id, NotFound, AlreadyExists

class ChannelResource(Resource):

    channel_id = fields.CharField(attribute='id', default=None)
    title = fields.CharField(attribute='title', default=None)
    comment = fields.CharField(attribute='comment', default=None)
    thumbnail_url = fields.CharField(attribute='thumbnail_url', default=None)
    podcasts = fields.ListField(attribute='podcasts', default=None)
    
    class Meta :
        resource_name = 'channels'
        include_resource_uri = False
        
    def obj_get(self, bundle, **kwargs):
        print("obj_get")
        channel_store = FileChannelStore()
        channel_id = kwargs.get('channel_id')
        try :
            return channel_store.get_channel(channel_id)
        except NotFound :
            raise ImmediateHttpResponse(response=HttpNotFound())

    def obj_get_list(self, bundle, **kwargs):
        channel_store = FileChannelStore()
        # map(channel_store.get, channel_store.get_channel_id_list())
        return [ channel_store.get_channel(channel_id) for channel_id in channel_store.get_channel_id_list() ]

    # def patch_detail(self, bundle, **kwargs):
    #     print("patch_detail",bundle,kwargs)
    #     channel_id = kwargs.get('channel_id')
    #     podcast_id = kwargs.get('podcast_id')
    #     channel = None
    #     if Channel.exists(channel_id) :
    #         channel = Channel(channel_id)
    #         channel.add_podcast(podcast_id)
    #     else :
    #         raise NotFound("Channel object not found")
    #     return channel

    def obj_create(self, bundle, **kwargs):
        #print("obj_create, begin bundle.obj=", bundle.obj)
        #print("obj_create, begin bundle.data=", bundle.data)
        # Populate bundle.obj with updated data from bundle.data
        channel_store = FileChannelStore()
        try :
            bundle.obj = channel_store.create_channel(**bundle.data)
        except AlreadyExists as e :
            #print("obj_create : already exists", bundle.data)
            bundle.obj = e.obj
            raise ImmediateHttpResponse(response=HttpConflict())
        
        channel_store.save_channel(bundle.obj)
        return bundle


    def obj_update(self, bundle, **kwargs):
        #print("obj_update, begin bundle.obj=", bundle.obj)
        #print("obj_update, begin bundle.data=", bundle.data)
        if bundle.obj == None : 
            # with patch method, obj_get is already called, in put method, i call it manually
            bundle.obj = self.obj_get(bundle, **kwargs)
        self.full_hydrate(bundle)
        #print("obj_update, full_hydrate bundle.obj=", bundle.obj)
        #print("obj_update, full_hydrate bundle.data=", bundle.data)

        channel_store = FileChannelStore()
        bundle.obj = channel_store.update_channel(channel=bundle.obj, update_data = bundle.data)
        channel_store.save_channel(bundle.obj)

        return bundle


    def obj_delete(self, bundle, **kwargs):
        print("obj_delete, begin bundle.obj=", bundle.obj)
        #print("obj_delete, begin bundle.data=", bundle.data)
        #print("obj_delete, begin kwargs=", kwargs)
        channel = self.obj_get(bundle, **kwargs)
        print("obj_delete, channel=", channel)
        channel_store = FileChannelStore()
        channel_store.delete_channel(channel)
        return bundle
       


