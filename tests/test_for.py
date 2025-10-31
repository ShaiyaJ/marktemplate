import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from marktemplate import processRaw

class ForTests(unittest.TestCase):
    def test_start_stop_step(self):
        RAW = """
<root test="ok">
    <mt-for start="1" stop="10" step="2">
        <mt-attr name="i" />
    </mt-for>
</root>
"""

        EXPECTED = """
<root test="ok">
    1
    3
    5
    7
    9
</root> 
"""

        self.assertEqual("".join(processRaw(RAW).split()), "".join(EXPECTED.split()))

    def test_invalid_datatype(self):
        RAW = """
<root test="ok">
    <mt-for from="s" to="g">
        <mt-attr name="i" />
    </mt-for>
</root>
"""

        with self.assertRaises(ValueError):
            processRaw(RAW)

    def test_custom_attr(self):
        RAW = """
<root test="ok">
    <mt-for name="x" start="1" stop="10">
        <mt-attr name="x" />
    </mt-for>
</root>
"""

        EXPECTED = """
<root test="ok">
    1
    2
    3
    4
    5
    6
    7
    8
    9
</root> 
"""
        
        self.assertEqual("".join(processRaw(RAW).split()), "".join(EXPECTED.split()))
