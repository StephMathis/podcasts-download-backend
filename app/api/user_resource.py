#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

from six import u
from tastypie import fields
from tastypie.resources import Resource

from ..lib.resources.default_meta_mixin import DefaultMetaMixin
from ..models.user import User


class UserResource(Resource):

    id = fields.CharField(attribute='id', default=None)
    first_name = fields.CharField(attribute='first_name', default=None)
    last_name = fields.CharField(attribute='last_name', default=None)

    class Meta(DefaultMetaMixin):

        resource_name = 'users'

    def obj_get_list(self, bundle, **kwargs):

        return [
            User(id=u("123456"), first_name=u("Foo"))
        ]
