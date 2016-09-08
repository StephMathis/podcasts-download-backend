#-*- coding: utf-8 -*-
#
# (c) 2013-2016 Wishtack
#
# $Id: $
#

import unittest

from tastypie.test import ResourceTestCaseMixin


class WtTestCase(ResourceTestCaseMixin, unittest.TestCase):

    def setUp(self):

        super(WtTestCase, self).setUp()

        self.maxDiff = None
