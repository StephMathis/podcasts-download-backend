# -*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

import base64

from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpNotFound
from tastypie.resources import Resource

from django.conf.urls import url
from django.http import StreamingHttpResponse

from .wish.wish_resource import WishResource
from ..lib.resources.default_meta_mixin import DefaultMetaMixin
from ..lib.resources.url_helper import UrlHelper
from ..models.podcast_item import PodcastItem


# http://localhost:8000/api/v1/podcasts/?url=aHR0cDovL2FwaS5ldXJvcGUxLmZyL3BvZGNhc3QvbXAzL2l0dW5lcy00MjM1MzQ4MDYvMjg1MDgxMS9wb2RjYXN0Lm1wMyZmaWxlbmFtZT1BQ0RIXy1fTCdpbnTDqWdyYWxlXzE5LzA5LzIwMTZfLV9MJ8OpdmFzaW9uX2QnSGVucmlfTWFzZXJzX2RlX0xhdHVkZS5tcDM=
# http://localhost:8000/api/v1/podcasts/?url=aHR0cDovL21lZGlhLnJhZGlvZnJhbmNlLXBvZGNhc3QubmV0L3BvZGNhc3QwOS8xODk5Ni0xOC4wOS4yMDE2LUlURU1BXzIxMDc5NDc0LTAubXAz
# http://localhost:8000/api/v1/podcasts/aHR0cDovL21lZGlhLnJhZGlvZnJhbmNlLXBvZGNhc3QubmV0L3BvZGNhc3QwOS8xODk5Ni0xOC4wOS4yMDE2LUlURU1BXzIxMDc5NDc0LTAubXAz/


class PodcastItemResource(Resource):

    #theurl = fields.CharField(attribute='url', default=None)
    item_url = fields.CharField(attribute='url', default=None)
    size = fields.CharField(attribute='size', default=None)

    class Meta :
        resource_name = 'items'

    def obj_get(self, bundle, **kwargs):
        item_id = kwargs.get('pk')
        item_url = base64.urlsafe_b64decode(item_id).decode("utf-8")
        item = PodcastItem(item_id)
        item.url = item_url
        
        #aa = "" #dict:%s-%d" % (kwargs,len(kwargs))
        #aa = kwargs.get('pk')
        #print(bundle.request.GET)
        fields_txt = bundle.request.GET.get('fields',None)
        if fields_txt :
            fields = fields_txt.split(',')
            if 'size' in fields :
                item.read_headers()
        return item

        
    def obj_get_list(self, bundle, **kwargs):
        theurl = base64.urlsafe_b64decode(bundle.request.GET['url']).decode("utf-8") 
        print("toto", bundle.request.GET['url'], theurl)
        p1 = PodcastItem("p1")
        p1.setUrl(theurl)
        return [p1,PodcastItem("salut le podcast 2")]

    def get_mp3(self, bundle, **kwargs) :
        item_id = kwargs.get('pk')
        item_url = base64.urlsafe_b64decode(item_id).decode("utf-8")
        item = PodcastItem(item_id)
        item.url = item_url
        resp = StreamingHttpResponse(item.read(), content_type=item.content_type)
        resp["Content-Disposition"] = 'attachment; filename="ZeFichier.mp3"'
        return resp


    def prepend_urls(self):
        return [
        #url to download mp3 file.
        url(r"^(?P<resource_name>%s)/(?P<pk>\w+)/content/$"% self._meta.resource_name,
                self.wrap_view('get_mp3'), name="api_get_mp3"),
        ]