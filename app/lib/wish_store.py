#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

from six import u

from ..models.wish import Wish


class WishStore(object):

    def wish_list(self, user_id):

        return [
            Wish(id=u("WISH123456"), title=u"Test")
        ]
