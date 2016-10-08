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

from .episode_resource import EpisodeResource

# http://localhost:8000/api/v1/podcasts/?url=aHR0cDovL2FwaS5ldXJvcGUxLmZyL3BvZGNhc3QvbXAzL2l0dW5lcy00MjM1MzQ4MDYvMjg1MDgxMS9wb2RjYXN0Lm1wMyZmaWxlbmFtZT1BQ0RIXy1fTCdpbnTDqWdyYWxlXzE5LzA5LzIwMTZfLV9MJ8OpdmFzaW9uX2QnSGVucmlfTWFzZXJzX2RlX0xhdHVkZS5tcDM=
# http://localhost:8000/api/v1/podcasts/?url=aHR0cDovL21lZGlhLnJhZGlvZnJhbmNlLXBvZGNhc3QubmV0L3BvZGNhc3QwOS8xODk5Ni0xOC4wOS4yMDE2LUlURU1BXzIxMDc5NDc0LTAubXAz
# http://localhost:8000/api/v1/podcasts/aHR0cDovL21lZGlhLnJhZGlvZnJhbmNlLXBvZGNhc3QubmV0L3BvZGNhc3QwOS8xODk5Ni0xOC4wOS4yMDE2LUlURU1BXzIxMDc5NDc0LTAubXAz/


class PodcastResource(Resource):

    #theurl = fields.CharField(attribute='url', default=None)
    podcast_url = fields.CharField(attribute='url', default=None)
    podcast_id = fields.CharField(attribute='id', default=None)
    content = fields.DictField(attribute='content', default=None)
    episodes = fields.ToManyField(
        to=EpisodeResource,
        attribute=lambda bundle: Podcast(bundle.obj.id).get_episodes(),
        full=True,
        readonly=True
    )

    class Meta :
        resource_name = 'podcasts'
        include_resource_uri = False

    def obj_get(self, bundle, **kwargs):
        pod_id = kwargs.get('pk')
        podcast = Podcast(pod_id)
        podcast.get_content()
        return podcast

        
    def obj_get_list(self, bundle, **kwargs):
        res = []
        for podcast_id in ["aHR0cDovL3JhZGlvZnJhbmNlLXBvZGNhc3QubmV0L3BvZGNhc3QwOS9yc3NfMTU2NDQueG1s","aHR0cDovL3JhZGlvZnJhbmNlLXBvZGNhc3QubmV0L3BvZGNhc3QwOS9yc3NfMTg5OTYueG1s"] :
            podcast = Podcast(podcast_id)
            podcast.get_content()
            res.append(podcast)
        return res


    def prepend_urls(self):
        return [
            UrlHelper().resource_url(
                rest_url='podcasts/:podcast_id/episodes',
                child_resource=EpisodeResource(),
                dispatch='dispatch_list'
            ),
            UrlHelper().resource_url(
                rest_url='podcasts/:podcast_id/episodes/:episode_id',
                child_resource=EpisodeResource(),
                dispatch='dispatch_detail'
            ),
            UrlHelper().resource_url(
                rest_url='podcasts/:podcast_id/episodes/:episode_id/content',
                child_resource=EpisodeResource(),
                dispatch='get_mp3'
            )
        ]
