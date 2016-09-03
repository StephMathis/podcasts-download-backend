#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

from synthetic import synthesize_constructor
from synthetic import synthesize_property


@synthesize_constructor()
@synthesize_property('id', contract='string|None')
@synthesize_property('first_name', contract='string|None')
@synthesize_property('last_name', contract='string|None')
class User(object):
    pass
