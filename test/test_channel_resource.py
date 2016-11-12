# -*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

from mock import patch
from six import u

from app.models.channel import Channel
from .lib.test_case import WtTestCase


class TestChannelResource(WtTestCase):

    def setUp(self):
        super(TestChannelResource, self).setUp()
        self._reset()

    def tearDown(self):
        super(TestChannelResource, self).tearDown()
        self._reset()

    @patch.object(UserStore, 'user_list')
    def test_should_get_channel_list(self, mock_user_list):
        mock_user_list.return_value = [
            User(
                id=u("user_1"),
                first_name=u("Foo")
            ),
            User(
                id=u("user_2"),
                first_name=u("John")
            )
        ]

        response = self.api_client.get('/podcast-api/v1/channels/')
        self.assertHttpOK(response)

        data = self.deserialize(response)

        self.assertEqual({
            u'meta': {
                u'limit': 20,
                u'next': None,
                u'offset': 0,
                u'previous': None,
                u'totalCount': 2},
            u'objects': [
                {
                    u'firstName': u'Foo',
                    u'id': u'user_1',
                    u'lastName': None,
                    u'resourceUri': u'/api/v1/users/user_1/',
                    u'wishes': [
                        {
                            u'id': u'WISH123456',
                            u'resourceUri': u'/api/v1/wishes/WISH123456/',
                            u'title': u'Test'
                        }
                    ]
                },
                {
                    u'firstName': u'John',
                    u'id': u'user_2',
                    u'lastName': None,
                    u'resourceUri': u'/api/v1/users/user_2/',
                    u'wishes': [
                        {
                            u'id': u'WISH123456',
                            u'resourceUri': u'/api/v1/wishes/WISH123456/',
                            u'title': u'Test'
                        }
                    ]
                }
            ]
        }, data)

    def test_should_add_user(self):

        user_store = UserStore()

        response = self.api_client.post(
            uri='/api/v1/users/',
            data={
                'firstName': u("Foo")
            }
        )

        self.assertHttpCreated(response)

        data = self.deserialize(response)

        self.assertEqual(1, len(user_store.user_list()))

        user_id = user_store.user_list()[0].id

        self.assertEqual({
            u'firstName': u'Foo',
            u'id': user_id,
            u'lastName': None,
            u'resourceUri': u'/api/v1/users/{}/'.format(user_id),
            u'wishes': [
                {
                    u'id': u'WISH123456',
                    u'resourceUri': u'/api/v1/wishes/WISH123456/',
                    u'title': u'Test'
                }
            ]
        }, data)

    def test_should_delete_user(self):

        user_store = UserStore()

        foo = user_store.create_user(user=User(first_name=u("Foo")))
        user_store.create_user(user=User(first_name=u("John")))

        response = self.api_client.delete(uri='/api/v1/users/{}/'.format(foo.id))

        self.assertHttpAccepted(response)

        self.assertEqual(1, len(user_store.user_list()))
        self.assertEqual(u("John"), user_store.user_list()[0].first_name)

    def _reset(self):
        pass
