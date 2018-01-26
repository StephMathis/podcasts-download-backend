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

from ..lib.tools import id2text, text2id, NotFound, AlreadyExists, ShouldNotBeCalled


class Channel(ModelMixin):
    def __init__(self, id, **kargs) :
        self.id = id
        self.title = kargs.get('title',"no title")
        self.comment = kargs.get('comment',"no comment")
        self.thumbnail_url = kargs.get('thumbnail_url',"")
        self.podcasts = kargs.get('podcasts',[])
    
    def add_podcast(self, podcast_id) :
        if podcast_id not in self.podcasts :
            self.podcasts.append(podcast_id)
            # the caller has certainly to save the channel
    
    def remove_podcast(self, podcast_id) :
        if podcast_id in self.podcasts :
            self.podcasts.remove(podcast_id)
            # the caller has certainly to save the channel

    def __str__(self):
        return u"{id}-{title}-{comment}-{thumbnail_url}-{podcasts}".format(id=self.id,
                                                 title=self.title,
                                                 comment=self.comment,
                                                 thumbnail_url=self.thumbnail_url,
                                                 podcasts=self.podcasts)

class ChannelStore :
    def __init__(self):
        pass
    

    def get_channel_id_list(self) :
        raise ShouldNotBeCalled("get_channel_id_list in ChannelStore should be pure virtual")


    def exists(self, channel_id) :
        return channel_id in self.get_channel_id_list()
    

    def get_channel(self, channel_id) :
        raise ShouldNotBeCalled("get_channel in ChannelStore should be pure virtual")
    

    def create_channel(self, **kargs) :
        channel_id = None
        try :
            channel_id = self.title2id(kargs['title']) # title is require
        except KeyError :
            raise KeyError('missing "title"" argument to create a channel')

        if self.exists(channel_id) :
            raise AlreadyExists("The channel %s already exists !" % kargs['title'], self.get_channel(channel_id))

        return Channel(channel_id, **kargs)
    

    def delete_channel(self, channel) :
        raise ShouldNotBeCalled("get_channel in ChannelStore should be pure virtual")
    

    def update_channel(self, **kargs) :
        channel = kargs['channel']
        update_data = kargs['update_data']
        d = channel.__dict__.copy()
        d.update(update_data)
        d.pop('id')
        updated_channel = Channel(channel.id, **d)

        # the code here is just because the podcast_id cannot be 
        # computed by frontend
        if d.get('new_podcast_url') :
            new_podcast_url = d['new_podcast_url']
            new_podcast_id = text2id(new_podcast_url)
            updated_channel.add_podcast(new_podcast_id)

        return updated_channel


    def save_channel(self, channel) :
        raise ShouldNotBeCalled("save_channel in ChannelStore should be pure virtual")


    def id2title(self, id) :
        return id2text(id)
    

    def title2id(self, title) :
        return text2id(title) 


class FileChannelStore(ChannelStore) :
    def __init__(self) :
        if not os.path.exists(self._get_root_path()) :
            print("*** %s does not exist" % (self._get_root_path()))
            # TODO : throw an Exception
        

    def _get_root_path(self) :
        return getattr(settings, "CHANNEL_ROOT_PATH", None)
    

    def _get_path(self, channel_id) :
        return os.path.join(self._get_root_path(), channel_id)


    def get_channel_id_list(self) :
        channel_id_list = []
        for channel_id in os.listdir(self._get_root_path()) :
            channel_id_list.append(channel_id)
        return channel_id_list
    

    def exists(self, channel_id) :
        path = self._get_path(channel_id)
        return os.path.exists(path) and os.path.isfile(path) and not os.path.islink(path)


    def get_channel(self, channel_id) :
        if not self.exists(channel_id) :
            raise NotFound("channel %s was not found", channel_id)
        with open(self._get_path(channel_id)) as data_file:
            d = json.load(data_file)
            id = d.pop('id')
            channel = Channel(id, **d)
        return channel
 
    def delete_channel(self, channel) :
        path = self._get_path(channel.id)
        if self.exists(channel.id) :
            os.remove(path)
        else :
            raise NotFound("path %s corresponding to channel %s was not found", path, channel_id)
           

    def save_channel(self, channel) :
        #print("save_channel", channel)
        f = open(self._get_path(channel.id), 'w')
        f.write(json.dumps(channel.__dict__))
        f.close() 
