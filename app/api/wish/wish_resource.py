#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#
from django.core.urlresolvers import reverse
from tastypie import fields
from tastypie.resources import Resource

from ...lib.wish_store import WishStore
from ...lib.resources.default_meta_mixin import DefaultMetaMixin


class WishResource(Resource):

    id = fields.CharField(attribute='id', default=None)
    title = fields.CharField(attribute='title', default=None)

    class Meta(DefaultMetaMixin):

        resource_name = 'wishes'

    def obj_get_list(self, bundle, **kwargs):
        return WishStore().wish_list(user_id=kwargs.get('user_id'))
