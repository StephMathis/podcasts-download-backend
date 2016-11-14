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

        self.assertEqual('^/?$', url_helper._rest_url_to_regex(''))
        self.assertEqual('^/?$', url_helper._rest_url_to_regex('/'))
        # channels
        self.assertEqual('^channels/?$', url_helper._rest_url_to_regex('channels'))
        self.assertEqual('^channels/?$', url_helper._rest_url_to_regex('channels/'))
        self.assertEqual('^channels/(?P<channel_id>\\w[\\w=-]*)/?$', url_helper._rest_url_to_regex('channels/:channel_id'))
        # podcasts

        # episodes

    def test_rest_url_to_name(self):

        url_helper = UrlHelper()

        self.assertEqual('rest_api_list', url_helper._rest_url_to_name(''))
        self.assertEqual('rest_api_list', url_helper._rest_url_to_name('/'))
        self.assertEqual('rest_api_channels_list', url_helper._rest_url_to_name('channels'))
        self.assertEqual('rest_api_channels_list', url_helper._rest_url_to_name('channels/'))
        self.assertEqual('rest_api_channels_detail', url_helper._rest_url_to_name('channels/:channel_id'))
        self.assertEqual('rest_api_users_wishes_list', url_helper._rest_url_to_name('users/:user_id/wishes'))
        self.assertEqual('rest_api_users_wishes_detail', url_helper._rest_url_to_name('users/:user_id/wishes/:wish_id'))