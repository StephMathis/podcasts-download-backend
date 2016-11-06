#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#
import base64

def id2text(id) :
    return base64.urlsafe_b64decode(id).decode("utf-8")

def text2id(text) :
    return base64.urlsafe_b64encode(text.encode("utf-8")).decode("utf-8")
