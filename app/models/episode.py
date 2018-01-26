#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#
import base64
import requests
import unicodedata

from synthetic import synthesize_constructor
from synthetic import synthesize_property

from .mixins.model_mixin import ModelMixin

@synthesize_constructor()
@synthesize_property('id', contract='string|None')
@synthesize_property('url', contract='string|None')
@synthesize_property('size', contract='int|None')
@synthesize_property('content_type', contract='string|None')
class Episode(ModelMixin):
    def read_headers(self):
        """
            perform a HEAD on self.url
        """
        self.url = base64.urlsafe_b64decode(self.id).decode("utf-8")
        if self.size is None:
            req = requests.head(self.url)
            print(req.headers)
            self.size = int(req.headers.get('Content-Length', None))
            self.content_type = req.headers.get('Content-Type')

    def read(self):
        """
            perform a GET on self.url
        """
        req = requests.get(self.url, stream=True)
        return req.raw

    @staticmethod
    def construct_episode_from_podcast_dict(data) :
        """
        for the definition of data, see podcast.get_episode_dict
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
        episode = Episode()
        episode.id = base64.urlsafe_b64encode(data['guid'].encode("utf-8")).decode("utf-8")
        episode.url = data['guid']
        episode.duration = data['total_time']
        episode.title = data['title']
        episode.title_ascii = unicodedata.normalize('NFKD',episode.title).encode("ascii","ignore").decode("ascii")
        episode.subtitle = data['subtitle']
        episode.published = data['published']        
        episode.size = data['enclosures'][0]['file_size']
        if episode.size == -1 :
            # in some cases, (http://cdn1-europe1.new2.ladmedia.fr/var/exports/podcasts/sound/au-coeur-de-l-histoire.xml),
            # the file size is set to -1 ...
            episode.size = None 
        return episode

