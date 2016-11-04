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
from .trackergroup_resource import TrackerGroupResource
from .channel_resource import ChannelResource

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
        pod_id = kwargs.get('podcast_id')
        # print("=============> PodcastResource.obj_get: kwargs=",kwargs)
        # print("=============> PodcastResource.obj_get: pod_id=", pod_id)
        # print("=============> PodcastResource.obj_get: prepend_urls=", self.prepend_urls())
        
        podcast = Podcast(pod_id)
        podcast.get_content()
        return podcast

        
    def obj_get_list(self, bundle, **kwargs):
        res = []
        urls_hack = ["http://radiofrance-podcast.net/podcast09/rss_16634.xml",
                     "http://radiofrance-podcast.net/podcast09/rss_15644.xml",
                     "http://radiofrance-podcast.net/podcast09/rss_18996.xml",
                     "http://radiofrance-podcast.net/podcast09/rss_12734.xml",
                     "http://radiofrance-podcast.net/podcast09/rss_12097.xml",
                     "http://cdn3-europe1.new2.ladmedia.fr/var/exports/podcasts/sound/Aux-origines-Franck-Ferrand.xml",
                     "http://cdn1-europe1.new2.ladmedia.fr/var/exports/podcasts/sound/au-coeur-de-l-histoire.xml",
                     "http://cdn-europe1.new2.ladmedia.fr/var/exports/podcasts/sound/ledito-politique-dyves-threard.xml",
                     "http://radiofrance-podcast.net/podcast09/rss_10009.xml",
                     "http://radiofrance-podcast.net/podcast09/rss_16370.xml",
                     "http://radiofrance-podcast.net/podcast09/rss_11548.xml",
                     "http://radiofrance-podcast.net/podcast09/rss_11453.xml"]
        for podcast_url in urls_hack :
            podcast_id = base64.urlsafe_b64encode(podcast_url.encode("utf-8")).decode("utf-8")
            podcast = Podcast(podcast_id)
            podcast.get_content()
            res.append(podcast)
        return res


    def prepend_urls(self):
        return [
            UrlHelper().resource_url(
                rest_url='podcasts/:podcast_id',
                child_resource=PodcastResource(),
                dispatch='dispatch_detail'
            ),            
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
            ),
            UrlHelper().resource_url(
                rest_url='podcasts/:podcast_id/episodes/:episode_id/contentwithtracker/:tracker_id',
                child_resource=EpisodeResource(),
                dispatch='get_mp3'
            ),
            UrlHelper().resource_url(
                rest_url='trackergroups/:tracker_group_id',
                child_resource=TrackerGroupResource(),
                dispatch='dispatch_detail'
            ),
            UrlHelper().resource_url(
                rest_url='channels',
                child_resource=ChannelResource(),
                dispatch='dispatch_list'
            ),
            UrlHelper().resource_url(
                rest_url='channels/:channel_id',
                child_resource=ChannelResource(),
                dispatch='dispatch_detail'
            ),
            UrlHelper().resource_url(
                rest_url='channels/:channel_id/podcasts/:podcast_id',
                child_resource=ChannelResource(),
                dispatch='dispatch_detail'
            )
        ]

