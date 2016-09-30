#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#
import requests

from synthetic import synthesize_constructor
from synthetic import synthesize_property

from .mixins.model_mixin import ModelMixin


@synthesize_constructor()
@synthesize_property('id', contract='string|None')
@synthesize_property('url', contract='string|None')
@synthesize_property('size', contract='int|None')
@synthesize_property('content_type', contract='string|None')
class PodcastItem(ModelMixin):
    def read_headers(self) :
        if self.size == None :
            r = requests.head(self.url)
            print(r.headers)
            self.size = int(r.headers.get('Content-Length', None))
            self.content_type = r.headers.get('Content-Type')
    
    def read(self) :
        r = requests.get(self.url,stream=True)
        return r.raw

