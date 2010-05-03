# -*- coding: utf-8 -*-
import sys
import unittest

sys.path.append('..')

from htmlfilter import HTMLFilter

class TestFilter(unittest.TestCase):

    def setUp(self):
        self.hf = HTMLFilter()

    def test_basic(self):
        CASES = (
            ('', ''),
            ('hello!', 'hello!'),
            (u'déjà vu', u'déjà vu'),
        )
        for dirty, clean in CASES:
            self.assertEqual(self.hf.filter(dirty), clean)

    def test_balancingtags(self):
        CASES = (
            ('<strong>very strong</strong>', '<strong>very strong</strong>'),
            ('<strong\n  >very strong</strong>', '<strong>very strong</strong>'),
            ('<strong>very strong', '<strong>very strong</strong>'),
            ('very strong</strong>', 'very strong'),
            ('<strong><strong>very strong</strong>', '<strong></strong><strong>very strong</strong>'),
        )
        for dirty, clean in CASES:
            self.assertEqual(self.hf.filter(dirty), clean)


    def test_endslashes(self):
        CASES = (
            ('<br>','<br />'),
            ('<hr>','<hr />'),
            ('<img>','<img />'),
            ('<img src="">','<img />'),
            ('<img src="img.png">','<img src="img.png" />'),
            ('<img src="a">test</img>', '<img src="a" />test'),
        )
        for dirty, clean in CASES:
            self.assertEqual(self.hf.filter(dirty), clean)


    def test_attributes(self):
        CASES = (
            ('<img src="img.png" not_allowed="no" />','<img src="img.png" />'),
            ('<a href="#" style="dd">test</a>','<a href="#">test</a>'),
        )
        for dirty, clean in CASES:
            self.assertEqual(self.hf.filter(dirty), clean)


    def test_corruptedtags(self):
        CASES = (
            ('<img src="img.png"/','<img src="img.png" />'),
            ('<a href="" err<em>test</em><a>','<a href="#"><em>test</em></a><a></a>'),
        )
        for dirty, clean in CASES:
            self.assertEqual(self.hf.filter(dirty), clean)


    def test_scripttag(self):
        CASES = (
            ('<script', ''),
            ('<script atrr="val<', ''),
            ('<script attr="val<strong>hello', '<strong>hello</strong>'),
            ('<script<script>>', '>'),
            ('<<script>script<script>>','script>'),
            ('<<script><script>>','>'),
        )
        for dirty, clean in CASES:
            self.assertEqual(self.hf.filter(dirty), clean)


    def test_protocols(self):
        CASES = (
            ('<a href="http://test">bar</a>', '<a href="http://test">bar</a>'),
            ('<a href="ftp://test">bar</a>', '<a href="ftp://test">bar</a>'),
            ('<a href="mailto:test">bar</a>', '<a href="mailto:test">bar</a>'),
            ('<a href="javascript:test">bar</a>', '<a href="#javascript:test">bar</a>'),
            ('<a href="java'+'\t'+'script:test">bar</a>', '<a href="#java'+'\t'+'script:test">bar</a>'),
        )
        for dirty, clean in CASES:
            self.assertEqual(self.hf.filter(dirty), clean)


if __name__ == '__main__':
    unittest.main()
