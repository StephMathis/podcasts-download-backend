# -*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

import base64
#from GenericCache.GenericCache import GenericCache


from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpNotFound
from tastypie.resources import Resource

from django.conf.urls import url
from django.http import StreamingHttpResponse

from .wish.wish_resource import WishResource
from ..lib.resources.default_meta_mixin import DefaultMetaMixin
from ..lib.resources.url_helper import UrlHelper
from ..models.podcast import Podcast

from .podcast_item_resource import PodcastItemResource

# http://localhost:8000/api/v1/podcasts/?url=aHR0cDovL2FwaS5ldXJvcGUxLmZyL3BvZGNhc3QvbXAzL2l0dW5lcy00MjM1MzQ4MDYvMjg1MDgxMS9wb2RjYXN0Lm1wMyZmaWxlbmFtZT1BQ0RIXy1fTCdpbnTDqWdyYWxlXzE5LzA5LzIwMTZfLV9MJ8OpdmFzaW9uX2QnSGVucmlfTWFzZXJzX2RlX0xhdHVkZS5tcDM=
# http://localhost:8000/api/v1/podcasts/?url=aHR0cDovL21lZGlhLnJhZGlvZnJhbmNlLXBvZGNhc3QubmV0L3BvZGNhc3QwOS8xODk5Ni0xOC4wOS4yMDE2LUlURU1BXzIxMDc5NDc0LTAubXAz
# http://localhost:8000/api/v1/podcasts/aHR0cDovL21lZGlhLnJhZGlvZnJhbmNlLXBvZGNhc3QubmV0L3BvZGNhc3QwOS8xODk5Ni0xOC4wOS4yMDE2LUlURU1BXzIxMDc5NDc0LTAubXAz/


class PodcastResource(Resource):

    #theurl = fields.CharField(attribute='url', default=None)
    podcast_url = fields.CharField(attribute='url', default=None)
    content = fields.CharField(attribute='content', default=None)

    class Meta :
        resource_name = 'podcasts'

    def obj_get(self, bundle, **kwargs):
        pod_id = kwargs.get('pk')
        podcast = Podcast(pod_id)
        podcast.get_content()
        return podcast

        
    def obj_get_list(self, bundle, **kwargs):
        theurl = base64.urlsafe_b64decode(bundle.request.GET['url']).decode("utf-8") 
        print("toto", bundle.request.GET['url'], theurl)
        p1 = Podcast("p1")
        p1.setUrl(theurl)
        return [p1,Podcast("salut le podcast 2")]
