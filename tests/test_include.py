import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from marktemplate import processRaw
import xml

class IncludeTests(unittest.TestCase):
    def test_include_nonexistent_path(self):
        RAW = """
<root>
    <mt-include src="./averylongpaththatwillneverexist" />
</root>
"""

        with self.assertRaises(FileNotFoundError):
           processRaw(RAW)

    def test_include_text(self):
        RAW = """
<root>
    <mt-include src="./text/1.txt" />
</root>
"""

        with self.assertRaises(xml.parsers.expat.ExpatError):
           processRaw(RAW)

    def test_include_mt_xml(self):
        RAW = """
<root>
    <mt-include src="./text/2.txt" />
</root>
"""

        EXPECTED = """
<root>
    <div test="hi">
        hi
    </div>
</root>
"""

        self.assertEqual("".join(processRaw(RAW).split()), "".join(EXPECTED.split()))

    def test_include_html(self):
        RAW = """
<root>
    <mt-include src="./text/3.text" />
</root>
"""

        EXPECTED = """
<root>
    <h1>test</h1>
    <div>
        <span>test2</span>
    </div>
</root>
"""

        self.assertEqual("".join(processRaw(RAW).split()), "".join(EXPECTED.split()))
