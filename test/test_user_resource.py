# -*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

from mock import patch
from six import u

from app.lib.user_store import UserStore
from app.models.user import User
from .lib.test_case import WtTestCase


class TestUserResource(WtTestCase):
    @patch.object(UserStore, 'user_list')
    def test_should_get_user_list(self, mock_user_list):
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

        response = self.api_client.get('/api/v1/users/')
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
