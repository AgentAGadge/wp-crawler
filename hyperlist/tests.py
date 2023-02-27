"""
    Hyperlist app. tests.py for Django framework.
"""
from django.test import TestCase
from . import service
import os

class BuildServerStoragePathTestCase(TestCase):
    def test_build_server_storage_path(self):
        #Data set
        dataset = ('thepath', '', '1', 1, 'the/path', 'the\\path' )
        for relative_path in dataset:
          #Arrange
          expected = os.path.realpath('storage'+os.sep+str(relative_path))
          #Act
          result = service.build_server_storage_path(relative_path)
          #Assert
          self.assertEqual(result, expected)
