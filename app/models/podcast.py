#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#
import requests, urllib
import base64
from cachetools import LRUCache
import podcastparser
import io
import json

from synthetic import synthesize_constructor
from synthetic import synthesize_property

from .mixins.model_mixin import ModelMixin

from .episode import Episode

def get_url(urlb64encoded) :
    return base64.urlsafe_b64decode(urlb64encoded).decode("utf-8")

def get_podcast_parsed_content(urlb64encoded) :
    url = get_url(urlb64encoded)
    #r = requests.get(url,stream=True)
    #return podcastparser.parse(url, r.raw)
    filelike = io.StringIO(requests.get(url).content.decode("utf-8"))
    return podcastparser.parse(url, filelike)

global_cache = LRUCache(maxsize=50, missing=get_podcast_parsed_content)


@synthesize_property('id', contract='string|None')
#@synthesize_property('content', contract='dict|None')
class Podcast(ModelMixin):
    def __init__(self, id) :
        self.id = id
        self.url = get_url(self.id)
        self.content = global_cache[self.id]
        super()

    def get_content(self) :
        self.content = global_cache[self.id]
    
    def get_episode_dict(self, guid) :
        """
        {'description': 'durée : 00:02:02 - par : Frédéric BENIADA',
               'enclosures': [{'file_size': 2298848,
                               'mime_type': 'audio/mpeg',
                               'url': 'http://rf.proxycast.org/1176676304313917440/18996-19.06.2016-ITEMA_21013689-0.mp3'}],
               'guid': 'http://media.radiofrance-podcast.net/podcast09/18996-19.06.2016-ITEMA_21013689-0.mp3',
               'link': 'http://www.france-info.com/',
               'payment_url': None,
               'published': 1466315100,
               'subtitle': 'Émission du 19.06.2016',
               'title': 'Chroniques du ciel 19.06.2016',
               'total_time': 122}
        """
        for episode in self.content['episodes'] :
            if guid == episode['guid'] :
                return episode
        return None


    def get_episodes(self) :
        res = []
        for episode_dict in self.content['episodes'] :
            res.append(Episode.construct_episode_from_podcast_dict(episode_dict))
        return res

            

