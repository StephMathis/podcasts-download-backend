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

from synthetic import synthesize_constructor
from synthetic import synthesize_property

from .mixins.model_mixin import ModelMixin

def get_podcast_parsed_content(urlb64encoded) :
    url = base64.urlsafe_b64decode(urlb64encoded).decode("utf-8")
    #r = requests.get(url,stream=True)
    #return podcastparser.parse(url, r.raw)
    filelike = io.StringIO()
    filelike.write(requests.get(url).content.decode("utf-8"))
    print(requests.get(url).content.decode("utf-8"))
    return podcastparser.parse(url, filelike)

    

global_cache = LRUCache(maxsize=50, missing=get_podcast_parsed_content)


@synthesize_property('id', contract='string|None')
@synthesize_property('content', contract='string|None')
class Podcast(ModelMixin):
    def __init__(self, id) :
        self.id = id
        super()

    def get_content(self) :
        self.content = "%s" % global_cache[self.id]

            

