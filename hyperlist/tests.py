"""
    Hyperlist app. tests.py for Django framework.
"""
import os

from urllib.error import URLError
from django.test import TestCase

from . import service

class GetSoupFromUrlErrorTestCase(TestCase):
    """Unit test of get_soup_from_url for exception returns"""
    def test_get_soup_from_url_not_url(self):
        """Pass a string as argument that is not a URL"""
        #Arrange
        expected = ValueError()
        #Act
        try:
            result = service.get_soup_from_url('toto')
        except ValueError as error:
            result = error
        #Assert
        self.assertEqual(type(expected),type(result))
    def test_get_soup_from_url(self):
        """Run the test"""
        #Arrange
        expected = URLError('test')
        #Act
        try:
            result = service.get_soup_from_url('http://www.juaezhfui.com')
        except URLError as error:
            result = error
        #Assert
        self.assertEqual(type(expected),type(result))

class BuildServerStoragePathTestCase(TestCase):
    """
    Unit test of build_server_storage_path
    """
    def test_build_server_storage_path(self):
        """Run the test"""
        #Data set
        dataset = ('thepath', '', '1', 1, 'the/path', 'the\\path' )
        for relative_path in dataset:
            #Arrange
            expected = os.path.realpath('storage'+os.sep+str(relative_path))
            #Act
            result = service.build_server_storage_path(relative_path)
            #Assert
            self.assertEqual(result, expected)

class GetStoredCrawlResultsTestCase(TestCase):
    """
    Unit test of get_storage_crawl_results
    """
    def equal_ignore_order(self, a, b):
        """Check that two lists contain the same values, possibly in a different order"""
        unmatched = list(b)
        for element in a:
            try:
                unmatched.remove(element)
            except ValueError:
                return False
        return not unmatched
    def test_get_stored_crawl_results(self):
        """Run the test"""
        #Arrange
        service.PATH_STORAGE = 'hyperlist/tests/storage'
        expected = [
            {'url': 'twitter.com', 'page': 'twitter.com/page.html'},
            {'url': 'www.twitter.com',
             'sitemap': 'www.twitter.com/sitemap.html',
             'page': 'www.twitter.com/page.html'},
            {'url': 'www.facebook.com',
             'sitemap': 'www.facebook.com/sitemap.html',
             'page': 'www.facebook.com/page.html'},
            {'url': 'www.google.fr',
             'sitemap': 'www.google.fr/sitemap.html',
             'page': 'www.google.fr/page.html'},
             {'url': 'www.google.com'},
            ]
        #Act
        result = service.get_stored_crawl_results()
        #Assert
        self.assertTrue(self.equal_ignore_order(result,expected))
