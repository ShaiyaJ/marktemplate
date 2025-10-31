import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from marktemplate import processRaw


class GlobTests(unittest.TestCase):
    def test_glob_all(self):
        RAW = """
<root>
    <mt-glob src="./text/*">
        <div><mt-attr name="src" /></div>
    </mt-glob>
</root>
"""

        EXPECTED = """
<root>
    <div src="./text/1.txt">./text/1.txt</div>
    <div src="./text/2.txt">./text/2.txt</div>
    <div src="./text/3.text">./text/3.text</div>
</root>
"""

        self.assertEqual("".join(processRaw(RAW).split()), "".join(EXPECTED.split()))

    def test_glob_filetype_wildcard(self):
        RAW = """
<root>
    <mt-glob src="./text/*.txt">
        <div><mt-attr name="src" /></div>
    </mt-glob>
</root>
"""

        EXPECTED = """
<root>
    <div src="./text/1.txt">./text/1.txt</div>
    <div src="./text/2.txt">./text/2.txt</div>
</root>
"""

        self.assertEqual("".join(processRaw(RAW).split()), "".join(EXPECTED.split()))


    def test_glob_nonexistent_path(self):
        RAW = """
<root>
    <mt-glob src="./areallylongpathnamewhichwillneverexist/*">
        <div><mt-attr name="src" /></div>
    </mt-glob>
</root>
"""

        EXPECTED = "<root></root>"

        self.assertEqual("".join(processRaw(RAW).split()), EXPECTED)
