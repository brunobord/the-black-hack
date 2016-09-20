from unittest import TestCase
from ..core import Builder


class DirListTest(TestCase):

    def setUp(self):
        super(DirListTest, self).setUp()
        self.builder = Builder()

    def test_dir_list_exceptions(self):
        for directory in self.builder.dir_list:
            self.assertFalse(directory.startswith('.'), directory)

    def test_dir_list_english(self):
        dir_list = tuple(self.builder.dir_list)
        self.assertIn('english', dir_list)
        self.assertEqual('english', dir_list[0])
