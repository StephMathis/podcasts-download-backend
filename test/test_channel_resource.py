# -*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

import os, shutil
from mock import patch
from six import u

from app.models.channel import Channel, ChannelStore, FileChannelStore
from .lib.test_case import WtTestCase


class TestChannelResource(WtTestCase):
    
    VAR_CHANNEL_DIR = "/tmp/podcasts-backend-test"

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        if os.path.exists(TestChannelResource.VAR_CHANNEL_DIR) :
            shutil.rmtree(TestChannelResource.VAR_CHANNEL_DIR)
        os.mkdir(TestChannelResource.VAR_CHANNEL_DIR)
        super(TestChannelResource, self).setUp()
        self._reset()

    def tearDown(self):
        super(TestChannelResource, self).tearDown()
        self._reset()

    @patch.object(FileChannelStore, '_get_root_path')
    def test_should_get_podcast(self, mock__get_root_path):
        mock__get_root_path.return_value = TestChannelResource.VAR_CHANNEL_DIR
        print("======================= test_should_get_podcast")
        response = self.api_client.get('/podcast-api/v1/podcasts/aHR0cDovL3JhZGlvZnJhbmNlLXBvZGNhc3QubmV0L3BvZGNhc3QwOS9yc3NfMTgyOTcueG1s')
        #response = self.api_client.get('/podcast-api/v1/podcasts/aHR0cDovL3JhZGlvZnJhbmNlLXBvZGNhc3QubmV0L3BvZGNhc3QwOS9yc3NfMTU2NDQueG1s')
        self.assertHttpOK(response)

        data = self.deserialize(response)

        self.assertEqual({
            'content': {'cover_url': 'http://media.radiofrance-podcast.net/podcast09/logo_1007.jpg',
                    'description': "Chaque jour un groupe d'enfants nous donne ses "
                                    'réponses aux grandes questions de la vie '
                                    'quotidienne.',
                    'episodes': [],
                    'link': 'http://www.radiofrance.fr/',
                    'title': "FB Cotentin Les p'tits Saint-Lois"},
            'episodes': [],
            'podcast_id': 'aHR0cDovL3JhZGlvZnJhbmNlLXBvZGNhc3QubmV0L3BvZGNhc3QwOS9yc3NfMTgyOTcueG1s',
            'podcast_url': 'http://radiofrance-podcast.net/podcast09/rss_18297.xml'
            }, data)  



    @patch.object(FileChannelStore, '_get_root_path')
    def test_should_get_empty_channel_list(self, mock__get_root_path):
        mock__get_root_path.return_value = TestChannelResource.VAR_CHANNEL_DIR

        print("======================= test_should_get_empty_channel_list")
        response = self.api_client.get('/podcast-api/v1/channels')
        self.assertHttpOK(response)

        data = self.deserialize(response)

        self.assertEqual({
            u'meta': {
                u'limit': 20,
                u'next': None,
                u'offset': 0,
                u'previous': None,
                u'total_count': 0},
            u'objects': []          
        }, data)    

    @patch.object(FileChannelStore, '_get_root_path')
    def test_should_create_channel_and_check_it_exits(self, mock__get_root_path):
        mock__get_root_path.return_value = TestChannelResource.VAR_CHANNEL_DIR
        print("======================= test_should_create_channel_and_check_it_exits")
        response = self.api_client.post(
            uri='/podcast-api/v1/channels',
            data={
                'title': u("Une chaine d'histoire")
            }
        )
        self.assertHttpCreated(response)
        self.assertEqual(b'',response.content) # no body in the response, just headers

        # check if the channel has been created
        response = self.api_client.get('/podcast-api/v1/channels')
        self.assertHttpOK(response)

        data = self.deserialize(response)

        self.assertEqual({
            u'meta': {
                u'limit': 20,
                u'next': None,
                u'offset': 0,
                u'previous': None,
                u'total_count': 1},
            u'objects': [{'channel_id': 'VW5lIGNoYWluZSBkJ2hpc3RvaXJl',
                          'comment': 'no comment',
                          'podcasts': [],
                          'thumbnail_url': '',
                          'title': "Une chaine d'histoire"}]         
        }, data)


    @patch.object(FileChannelStore, '_get_root_path')
    def test_should_reject_when_try_creating_existing_channel(self, mock__get_root_path) :
        mock__get_root_path.return_value = TestChannelResource.VAR_CHANNEL_DIR
        print("======================= test_should_reject_when_try_creating_existing_channel")

        response = self.api_client.post(
            uri='/podcast-api/v1/channels',
            data={
                'title': u("Une chaine d'histoire")
            }
        )

        self.assertHttpCreated(response)
        response = self.api_client.post(
            uri='/podcast-api/v1/channels',
            data={
                'title': u"Une chaine d'histoire",
                'comment': u'this is a significant comment',
                'podcasts': ['aaa','bbb'],
                'thumbnail_url': u'image_url'
            }
        )
        self.assertHttpConflict(response)
        self.assertEqual(b'',response.content) # no body in the response, just headers

        # check if the existing channel has not been modified
        response = self.api_client.get('/podcast-api/v1/channels')
        self.assertHttpOK(response)

        data = self.deserialize(response)

        self.assertEqual({
            u'meta': {
                u'limit': 20,
                u'next': None,
                u'offset': 0,
                u'previous': None,
                u'total_count': 1},
            u'objects': [{'channel_id': 'VW5lIGNoYWluZSBkJ2hpc3RvaXJl',
                          'comment': 'no comment',
                          'podcasts': [],
                          'thumbnail_url': '',
                          'title': "Une chaine d'histoire"}]         
        }, data)
    


    @patch.object(FileChannelStore, '_get_root_path')
    def test_should_put_exising_channel(self, mock__get_root_path) :
        mock__get_root_path.return_value = TestChannelResource.VAR_CHANNEL_DIR

        print("======================= test_should_put_exising_channel")
        response = self.api_client.post(
            uri='/podcast-api/v1/channels',
            data={
                'title': u"Une chaine d'histoire",
                'comment': u'this is a significant comment',
                'podcasts': ['aaa','bbb'],
                'thumbnail_url': u'image_url'
            }
        )
        self.assertHttpCreated(response)

        response = self.api_client.get('/podcast-api/v1/channels/VW5lIGNoYWluZSBkJ2hpc3RvaXJl')
        self.assertHttpOK(response)

        response = self.api_client.put(
            uri='/podcast-api/v1/channels/VW5lIGNoYWluZSBkJ2hpc3RvaXJl',
            data={
                'title': u"Une chaine d'histoire modified",
                'comment': u'this is a UNsignificant comment',
                'podcasts': ['aaa'],
                'new_podcast_url': u'ccc',
                'thumbnail_url': u'image_url2'
            }
        )
        self.assertHttpAccepted(response) # 202 Accepted
        self.assertEqual(b'',response.content) # no body in the response, just headers

        # check if the existing channel has not been modified
        response = self.api_client.get('/podcast-api/v1/channels')
        self.assertHttpOK(response)

        data = self.deserialize(response)

        self.assertEqual({
            u'meta': {
                u'limit': 20,
                u'next': None,
                u'offset': 0,
                u'previous': None,
                u'total_count': 1},
            u'objects': [{'channel_id': 'VW5lIGNoYWluZSBkJ2hpc3RvaXJl',
                          'comment': 'this is a UNsignificant comment',
                          'podcasts': ['aaa', 'Y2Nj'],
                          'thumbnail_url': 'image_url2',
                          'title': "Une chaine d'histoire modified"}]         
        }, data)

        response = self.api_client.delete('/podcast-api/v1/channels/VW5lIGNoYWluZSBkJ2hpc3RvaXJl/podcasts/aaa')
        self.assertHttpAccepted(response)
        response = self.api_client.get('/podcast-api/v1/channels/VW5lIGNoYWluZSBkJ2hpc3RvaXJl')
        self.assertHttpOK(response)
        print(response)
        data = self.deserialize(response)
        self.assertEqual({
                 'channel_id': u'VW5lIGNoYWluZSBkJ2hpc3RvaXJl',
                 'title': u"Une chaine d'histoire modified",
                 'comment': u'this is a UNsignificant comment',
                 'podcasts': ['Y2Nj'],
                 'thumbnail_url': u'image_url2'
            }, data)    


    @patch.object(FileChannelStore, '_get_root_path')
    def test_should_delete_exising_channel(self, mock__get_root_path) :
        mock__get_root_path.return_value = TestChannelResource.VAR_CHANNEL_DIR

        print("======================= test_should_delete_exising_channel")
        response = self.api_client.post(
            uri='/podcast-api/v1/channels',
            data={
                'title': u"Une chaine d'histoire",
                'comment': u'this is a significant comment',
                'podcasts': ['aaa'],
                'thumbnail_url': u'image_url'
            }
        )
        self.assertHttpCreated(response)

        response = self.api_client.delete(uri='/podcast-api/v1/channels/{}/'.format('VW5lIGNoYWluZSBkJ2hpc3RvaXJl'))
        self.assertHttpAccepted(response) # 204 No content

        response = self.api_client.get('/podcast-api/v1/channels')
        self.assertHttpOK(response)

        data = self.deserialize(response)

        self.assertEqual({
            u'meta': {
                u'limit': 20,
                u'next': None,
                u'offset': 0,
                u'previous': None,
                u'total_count': 0},
            u'objects': []          
        }, data)         


    def _reset(self):
        pass
