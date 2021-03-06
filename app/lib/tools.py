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


class PodcastsError(Exception):
    """A base exception for other tastypie-related errors."""
    pass

class NotYetImplemented(PodcastsError) :
    pass

class ShouldNotBeCalled(PodcastsError) :
    pass

class NotFound(PodcastsError):
    """
    Raised when the resource/object in question can't be found.
    """
    pass

class AlreadyExists(PodcastsError):
    """
    Raised when the resource/object already exists
    """
    def __init__(self, message, obj):
        self.message = message
        self.obj = obj