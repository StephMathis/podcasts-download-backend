#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#


class ModelMixin(object):

    @property
    def pk(self):
        return getattr(self, 'id')

    @pk.setter
    def pk(self, pk):
        setattr(self, 'id', pk)
