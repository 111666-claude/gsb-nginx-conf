import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nginxconf import core

TEXT = "root /var/www;\n"


class NginxConfTest(unittest.TestCase):
    def test_root_block(self):
        root = core.parse("", {}, core.Counter())
        self.assertEqual(root.name, "")

    def test_directive_parsed(self):
        root = core.parse(TEXT, {}, core.Counter())
        self.assertEqual(len(root.directives), 1)

    def test_directive_key(self):
        root = core.parse(TEXT, {}, core.Counter())
        self.assertEqual(root.directives[0][0], "root")

    def test_child_block(self):
        root = core.parse("server {\n}\n", {}, core.Counter())
        self.assertEqual(len(root.children), 1)

    def test_comment_skipped(self):
        root = core.parse("# c\n", {}, core.Counter())
        self.assertEqual(len(root.directives), 0)

    def test_counter_counts(self):
        counter = core.Counter()
        core.parse(TEXT, {}, counter)
        self.assertGreater(counter.scanned, 0)


if __name__ == "__main__":
    unittest.main()
