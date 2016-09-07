#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

from six import u

from ..models.user import User


class UserStore(object):

    def user_list(self):

        return [
            User(id=u("123456"), first_name=u("Foo"))
        ]

    def get_user(self, user_id):

        result_list = [user for user in self.user_list() if user.id == user_id]
        if len(result_list) > 0:
            return result_list[0]
        else:
            return None
