#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

from synthetic import synthesize_constructor
from synthetic import synthesize_property

from .mixins.model_mixin import ModelMixin


@synthesize_constructor()
@synthesize_property('id', contract='string|None')
@synthesize_property('first_name', contract='string|None')
@synthesize_property('last_name', contract='string|None')
class User(ModelMixin):
    pass

