import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from marktemplate import processRaw

class AttrTests(unittest.TestCase):
    def test_existant_attr(self):
        """Test for an existant attribute on a parent node"""

        RAW = """
<root test="ok">
    <mt-attr name="test" />
</root>
"""

        EXPECTED = """
<root test="ok">
    ok
</root>
"""

        self.assertEqual(processRaw(RAW).strip(), EXPECTED.strip())

    def test_nonexistant_attr(self):
        RAW = """
<root>
    <mt-attr name="test" />
</root>
"""

        with self.assertRaises(AttributeError):
            processRaw(RAW)

    def test_attr_on_attr_tag(self):
        """Test for an existant attribute on the attribute tag"""

        RAW = """
<root>
    <mt-attr test="ok" name="test" />
</root>
"""

        EXPECTED = """
<root>
    ok
</root>
"""

        self.assertEqual(processRaw(RAW).strip(), EXPECTED.strip())


    def test_overwritten_attr(self):
        """Testing for an existant attribute that gets overwritten - expecting the 'closest' tag to take priority"""

        RAW = """
<root test="not-ok">
    <child test="ok">
        <mt-attr name="test" />
    </child>
</root>
"""

        EXPECTED = """
<root test="not-ok">
    <child test="ok">
        ok
    </child>
</root>
"""

        self.assertEqual(processRaw(RAW).strip(), EXPECTED.strip())


if __name__ == "__main__":
    RAW = """
<root test="ok">
    <mt-attr name="test" />
</root>
"""
    print( processRaw(RAW) )


