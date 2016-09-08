#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

from app.lib.resources.camel_case_json_serializer import CamelCaseJsonSerializer


class DefaultMetaMixin(object):

    always_return_data = True
    detail_uri_name = 'id'
    serializer = CamelCaseJsonSerializer()
