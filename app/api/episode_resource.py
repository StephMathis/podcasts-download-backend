# -*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

import base64
import random

from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpNotFound
from tastypie.resources import Resource

from django.conf.urls import url
from django.http import StreamingHttpResponse

from .wish.wish_resource import WishResource
from ..lib.resources.default_meta_mixin import DefaultMetaMixin
from ..lib.resources.url_helper import UrlHelper
from ..models.episode import Episode
from ..models.podcast import Podcast
from ..models.download import Download

# http://localhost:8000/api/v1/podcasts/?url=aHR0cDovL2FwaS5ldXJvcGUxLmZyL3BvZGNhc3QvbXAzL2l0dW5lcy00MjM1MzQ4MDYvMjg1MDgxMS9wb2RjYXN0Lm1wMyZmaWxlbmFtZT1BQ0RIXy1fTCdpbnTDqWdyYWxlXzE5LzA5LzIwMTZfLV9MJ8OpdmFzaW9uX2QnSGVucmlfTWFzZXJzX2RlX0xhdHVkZS5tcDM=
# http://localhost:8000/api/v1/podcasts/?url=aHR0cDovL21lZGlhLnJhZGlvZnJhbmNlLXBvZGNhc3QubmV0L3BvZGNhc3QwOS8xODk5Ni0xOC4wOS4yMDE2LUlURU1BXzIxMDc5NDc0LTAubXAz
# http://localhost:8000/api/v1/podcasts/aHR0cDovL21lZGlhLnJhZGlvZnJhbmNlLXBvZGNhc3QubmV0L3BvZGNhc3QwOS8xODk5Ni0xOC4wOS4yMDE2LUlURU1BXzIxMDc5NDc0LTAubXAz/

EPISODES_REQUEST = {}


class EpisodeResource(Resource):

    #theurl = fields.CharField(attribute='url', default=None)
    episode_id = fields.CharField(attribute='id', default=None)
    source_url = fields.CharField(attribute='url', default=None)
    size = fields.CharField(attribute='size', default=None)
    title = fields.CharField(attribute='title', default=None)
    subtitle = fields.CharField(attribute='subtitle', default=None)
    duration = fields.CharField(attribute='duration', default=None)
    published = fields.CharField(attribute='published', default=None)
    
    class Meta :
        resource_name = 'episodes'
        include_resource_uri = False
        

    def _get_episode(self, podcast_id, episode_id) :
        podcast = Podcast(podcast_id)
        episode_url = base64.urlsafe_b64decode(episode_id).decode("utf-8")
        episode_dict = podcast.get_episode_dict(episode_url)
        episode = Episode.construct_episode_from_podcast_dict(episode_dict)

        return episode

    def obj_get(self, bundle, **kwargs):
        podcast_id = kwargs.get('podcast_id')
        episode_id = kwargs.get('episode_id')

        # fields_txt = bundle.request.GET.get('fields',None)
        # if fields_txt :
        #     fields = fields_txt.split(',')
        #     if 'size' in fields :
        #         episode.read_headers()
        print(kwargs)
        return self._get_episode(podcast_id, episode_id)

        
    def obj_get_list(self, bundle, **kwargs):
        return Podcast(kwargs.get('podcast_id')).get_episodes()

    def get_mp3(self, bundle, **kwargs) :
        podcast_id = kwargs.get('podcast_id')
        episode_id = kwargs.get('episode_id')
        download_id = kwargs.get('download_id')

        episode = self._get_episode(podcast_id, episode_id)    
        raw = episode.read()
        if download_id :
            download = Download(download_id)
            download.setCloseable(raw)
        resp = StreamingHttpResponse(raw, content_type=episode.content_type)
        resp["Content-Disposition"] = 'attachment; filename="%s.mp3"' % episode.title
        return resp

    def prepend_urls___(self):
        return [
        #url to download mp3 file.
        url(r"^(?P<resource_name>%s)/(?P<pk>\w+)/content/$"% self._meta.resource_name,
                self.wrap_view('get_mp3'), name="api_get_mp3"),
        ]