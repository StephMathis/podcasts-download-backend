#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

import re

from django.conf.urls import url
from tastypie.utils import trailing_slash


class UrlHelper(object):

    def resource_url(self, rest_url, child_resource, dispatch):

        return url(
            regex=self._rest_url_to_regex(rest_url=rest_url),
            view=child_resource.wrap_view(dispatch),
            name=self._rest_url_to_name(rest_url=rest_url)
        )

    def _is_rest_id_split(self, split):
        """
        :param split:
        :return: returns true for ':user_id' and false for 'users'.
        """
        return split.startswith(':')

    def _rest_url_to_name(self, rest_url):

        rest_url_split_list = self._split_rest_url(rest_url=rest_url)
        url_name = 'rest_api_'

        # Check if detail or list.
        is_detail = len(rest_url_split_list) > 0 and self._is_rest_id_split(rest_url_split_list[-1])

        rest_url_resource_name_list = [rest_url for rest_url in rest_url_split_list
                                       if not self._is_rest_id_split(rest_url)]

        for resource_name in rest_url_resource_name_list:
            url_name += '{resource_name}_'.format(resource_name=resource_name)

        url_name += '{suffix}'.format(suffix='detail' if is_detail else 'list')

        return url_name


    def _rest_url_to_regex(self, rest_url):

        rest_url_split_list = self._split_rest_url(rest_url=rest_url)
        regex_url = '^'

        for split in rest_url_split_list:

            # Resource id replacement.
            if self._is_rest_id_split(split=split):
                regex_url += r"(?P<{resource_id_name}>\w[\w=-]*)".format(resource_id_name=split[1:])

            # Resource name replacement.
            else:
                regex_url += split

            # Adding separator.
            regex_url += '/'

        # Remvoing trailing slash and adding it optionally then ending regex.
        regex_url = regex_url.rstrip('/') + trailing_slash() + '$'

        # Remove '/' duplicates.
        regex_url = re.sub(r"/+", '/', regex_url)

        return regex_url

    def _split_rest_url(self, rest_url):

        rest_url_split_list = rest_url.split('/')

        # Removing superfluous trailing splits.
        while len(rest_url_split_list) > 0 and len(rest_url_split_list[-1]) == 0:
            rest_url_split_list = rest_url_split_list[:-1]

        return rest_url_split_list
