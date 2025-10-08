import unittest

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from marktemplate import processRaw

class AttrTests(unittest.TestCase):
    def existant_attr(self):
        """Test for an existant attribute on a parent node"""

        RAW = """
<root test="ok">
    <attr name="test" />
</root>
"""

        EXPECTED = """
<root test="ok">
    ok
</root>
"""

        self.assertEqual(processRaw(RAW), EXPECTED)

    def nonexistant_attr(self):
        pass

    def attr_on_attr_tag(self):
        """Test for an existant attribute on the attribute tag"""

        RAW = """
<root>
    <attr test="ok" name="test" />
</root>
"""

        EXPECTED = """
<root>
    ok
</root>
"""

        self.assertEqual(processRaw(RAW), EXPECTED)


    def overwritten_attr(self):
        """Testing for an existant attribute that gets overwritten - expecting the 'closest' tag to take priority"""

        RAW = """
<root test="not-ok">
    <child test="ok">
        <attr name="test" />
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

        self.assertEqual(processRaw(RAW), EXPECTED)


if __name__ == "__main__":
    unittest.main()
