# -*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpNotFound
from tastypie.resources import Resource

from .wish.wish_resource import WishResource
from ..lib.resources.default_meta_mixin import DefaultMetaMixin
from ..lib.resources.url_helper import UrlHelper
from ..lib.user_store import UserStore
from ..lib.wish_store import WishStore
from ..models.user import User


class UserResource(Resource):

    id = fields.CharField(attribute='id', default=None)
    first_name = fields.CharField(attribute='first_name', default=None)
    last_name = fields.CharField(attribute='last_name', default=None)
    wishes = fields.ToManyField(
        to=WishResource,
        attribute=lambda bundle: WishStore().wish_list(user_id=bundle.obj.id),
        full=True,
        readonly=True
    )

    class Meta(DefaultMetaMixin):

        resource_name = 'users'

    def obj_create(self, bundle, **kwargs):

        bundle.obj = UserStore().create_user(User(**bundle.data))

        return bundle

    def obj_delete(self, bundle, **kwargs):

        if not UserStore().remove_user(user_id=kwargs.get('id')):
            raise ImmediateHttpResponse(response=HttpNotFound())

        return None

    def obj_get(self, bundle, **kwargs):

        user = UserStore().find_user(user_id=kwargs.get('id'))

        if user is None:
            raise ImmediateHttpResponse(response=HttpNotFound())

        return user

    def obj_get_list(self, bundle, **kwargs):

        return UserStore().user_list()

    def prepend_urls(self):

        return [
            UrlHelper().resource_url(
                rest_url='users/:user_id/wishes',
                child_resource=WishResource()
            )
        ]
