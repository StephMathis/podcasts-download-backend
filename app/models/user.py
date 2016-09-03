#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

from synthetic import synthesize_constructor
from synthetic import synthesize_member


@synthesize_constructor()
@synthesize_member('first_name', contract='string|None')
@synthesize_member('last_name', contract='string|None')
class User(object):
    pass
