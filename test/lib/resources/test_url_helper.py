#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

import unittest

from app.lib.resources.url_helper import UrlHelper


class TestUrlHelper(unittest.TestCase):

    def test_rest_url_to_regex(self):

        url_helper = UrlHelper()

        self.assertEqual('^/$', url_helper._rest_url_to_regex(''))
        self.assertEqual('^/$', url_helper._rest_url_to_regex('/'))
        self.assertEqual('^users/$', url_helper._rest_url_to_regex('users'))
        self.assertEqual('^users/$', url_helper._rest_url_to_regex('users/'))
        self.assertEqual('^users/(?P<user_id>\\w[\\w/-]*)/$', url_helper._rest_url_to_regex('users/:user_id'))
        self.assertEqual('^users/(?P<user_id>\\w[\\w/-]*)/wishes/$',
                         url_helper._rest_url_to_regex('users/:user_id/wishes'))
        self.assertEqual('^users/(?P<user_id>\\w[\\w/-]*)/wishes/(?P<wish_id>\\w[\\w/-]*)/$',
                         url_helper._rest_url_to_regex('users/:user_id/wishes/:wish_id'))

    def test_rest_url_to_name(self):

        url_helper = UrlHelper()

        self.assertEqual('rest_api_list', url_helper._rest_url_to_name(''))
        self.assertEqual('rest_api_list', url_helper._rest_url_to_name('/'))
        self.assertEqual('rest_api_users_list', url_helper._rest_url_to_name('users'))
        self.assertEqual('rest_api_users_list', url_helper._rest_url_to_name('users/'))
        self.assertEqual('rest_api_users_detail', url_helper._rest_url_to_name('users/:user_id'))
        self.assertEqual('rest_api_users_wishes_list', url_helper._rest_url_to_name('users/:user_id/wishes'))
        self.assertEqual('rest_api_users_wishes_detail', url_helper._rest_url_to_name('users/:user_id/wishes/:wish_id'))