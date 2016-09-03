#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

from six import u
from tastypie import fields
from tastypie.resources import Resource

from ..models.user import User


class UserResource(Resource):

    first_name = fields.CharField(attribute='first_name', default=None)
    last_name = fields.CharField(attribute='last_name', default=None)

    class Meta:
        resource_name = 'users'

    def obj_get_list(self, bundle, **kwargs):
        return [
            User(first_name=u("Foo"))
        ]
