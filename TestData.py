#!python3
#encoding:utf-8
import unittest
from Data import Data

import os.path
from configparser import ConfigParser, ExtendedInterpolation

class TestData(unittest.TestCase):
    def initialize(self):
        self.file_path_config = './config.ini'
        self.config = ConfigParser(interpolation=ExtendedInterpolation())
        self.config.read(self.file_path_config)
        self.data = Data()
    def test_get_username(self):
        self.initialize()
        self.assertEqual(self.data.get_username(), self.config['GitHub']['Username'])
    def test_get_ssh_host(self):
        self.initialize()
        self.assertEqual(self.data.get_ssh_host(), self.config['SSH']['Host'])
    def test_get_repo_name(self):
        self.initialize()
        self.assertEqual(self.data.get_repo_name(), os.path.basename(os.path.dirname(os.path.abspath(__file__))))
    def test_get_repo_description(self):
        self.initialize()
        self.assertEqual(self.data.get_repo_description(), self.config['Repository']['Description'])
    def test_get_repo_homepage(self):
        self.initialize()
        self.assertEqual(self.data.get_repo_homepage(), self.config['Repository']['Homepage'])
    def test_get_mail_address(self):
        self.initialize()
        self.assertEqual(self.data.get_mail_address(), "user1@mail.com")
    def test_get_access_token(self):
        self.initialize()
        self.assertEqual(self.data.get_access_token(['repo']), "this_is_access_token")

