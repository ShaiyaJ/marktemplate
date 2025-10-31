import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from marktemplate import processRaw
import xml
import html

class RawIncludeTests(unittest.TestCase):
    def test_include_nonexistent_path(self):
        RAW = """
<root>
    <mt-raw-include src="./averylongpaththatwillneverexist" />
</root>
"""

        with self.assertRaises(FileNotFoundError):
           processRaw(RAW)

    def test_include_text(self):
        RAW = """
<root>
    <mt-raw-include src="./text/1.txt" />
</root>
"""

        EXPECTED = """
<root>
    testtext
</root>
"""

        self.assertEqual("".join(processRaw(RAW).split()), "".join(EXPECTED.split()))

    def test_include_mt_xml(self):
        RAW = """
<root>
    <mt-raw-include src="./text/2.txt" />
</root>
"""

        EXPECTED = """
<root>
    &lt;root&gt;&lt;divtest="hi"&gt;&lt;mt-attrname="test"/&gt;&lt;/div&gt;&lt;/root&gt;
</root>
"""

        self.assertEqual("".join(processRaw(RAW).split()), "".join(EXPECTED.split()))

    def test_include_html(self):
        RAW = """
<root>
    <mt-raw-include src="./text/3.text" />
</root>
"""

        EXPECTED = """
<root>
    &lt;root&gt;&lt;h1&gt;test&lt;/h1&gt;&lt;div&gt;&lt;span&gt;test2&lt;/span&gt;&lt;/div&gt;&lt;/root&gt;
</root>
"""

        self.assertEqual("".join(processRaw(RAW).split()), "".join(EXPECTED.split()))
