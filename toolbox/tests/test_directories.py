from unittest import TestCase
from .. import Builder


class DirListTest(TestCase):

    def setUp(self):
        super(DirListTest, self).setUp()
        self.builder = Builder()

    def test_dir_list_exceptions(self):
        for directory in self.builder.dir_list:
            self.assertFalse(directory.startswith('.'), directory)
