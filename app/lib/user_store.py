#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

import copy

from bson import ObjectId
from contracts import contract, new_contract
from six import u

from ..models.user import User

new_contract('User', User)


class UserStore(object):

    _user_list = []

    @contract
    def create_user(self, user):
        """
        :type user: User
        :return: the created user (id from data source + canonicalization...)
        """
        user = copy.copy(user)
        user.id = str(ObjectId())
        self._user_list.append(user)
        return user

    @contract
    def find_user(self, user_id):
        """
        :type user_id: string
        :return: the user.
        """

        result_list = [user for user in self.user_list() if user.id == user_id]
        if len(result_list) > 0:
            return result_list[0]
        else:
            return None

    def remove_user(self, user_id):

        user = self.find_user(user_id=user_id)

        if user is not None:
            self._user_list.remove(user)
            return True
        else:
            return False

    def user_list(self):
        return self._user_list

    def reset(self):
        UserStore._user_list = []