#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#
import base64
import json
import os, os.path

from synthetic import synthesize_constructor
from synthetic import synthesize_property

from .mixins.model_mixin import ModelMixin
from django.conf import settings

class Channel(ModelMixin):
    def __init__(self, id) :
        self.id = id
        self.title = Channel.id2title(id)
        self.path = Channel.get_path(id)
        self.podcasts = None
        if not os.path.exists(Channel.get_root_path()) :
            print("*** %s does not exist" % (Channel.get_root_path()))
            # TODO : throw an Exception
        if not os.path.isfile(self.path) :
            # channel does not exist, it's a new one
            self.podcasts = []
            self._save()
        else :
            self._load()
    
    def _load(self) :
        if self.podcasts != None :
            return
                
        if         os.path.exists(self.path) \
           and     os.path.isfile(self.path) \
           and not os.path.islink(self.path) :
            with open(self.path) as data_file:    
                self.podcasts = json.load(data_file)
    
    def _save(self) :
        f = open(self.path,'w')
        f.write(json.dumps(self.podcasts))
        f.close()

    def get_title(self) :
        return Channel.id2title(self.id)

    def get_podcasts(self) :
        return self.podcasts
    
    def add_podcast(self, podcast_id) :
        if podcast_id not in self.podcasts :
            self.podcasts.append(podcast_id)
            self._save()

    @staticmethod
    def get_root_path() :
        return getattr(settings, "CHANNEL_ROOT_PATH", None)
    
    @staticmethod
    def get_path(channel_id) :
        return os.path.join(Channel.get_root_path(), channel_id)

    @staticmethod
    def id2title(id) :
        return base64.urlsafe_b64decode(id).decode("utf-8")
    
    @staticmethod
    def title2id(title) :
        return base64.urlsafe_b64encode(title.encode("utf-8")).decode("utf-8")

    @staticmethod
    def get_channels() :
        channels = []
        for channel_id in os.listdir(Channel.get_root_path()) :
            channels.append(Channel(channel_id))
        return channels
    
    @staticmethod
    def exists(channel_id) :
        return os.path.exists(Channel.get_path(channel_id)) 
            
        
        
            

