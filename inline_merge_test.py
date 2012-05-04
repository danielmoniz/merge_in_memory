import unittest

import inline_merge as merge_module

reload(merge_module)

class DiffTest(unittest.TestCase):
    def setUp(self):
        self.inline_merge = merge_module.InlineMerge()
        self.text1 = """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Integer
eu lacus accumsan arcu fermentum euismod. Donec pulvinar porttitor
tellus. Aliquam venenatis. Donec facilisis pharetra tortor.  In nec
mauris eget magna consequat convallis. Nam sed sem vitae odio
pellentesque interdum. Sed consequat viverra nisl. Suspendisse arcu
metus, blandit quis, rhoncus ac, pharetra eget, velit. Mauris
urna. Morbi nonummy molestie orci. Praesent nisi elit, fringilla ac,
suscipit non, tristique vel, mauris. Curabitur vel lorem id nisl porta
adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate tristique
enim. Donec quis lectus a justo imperdiet tempus."""

        self.text2 = """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Integer
eu lacus accumsan arcu fermentum euismod. Donec pulvinar, porttitor
tellus. Aliquam venenatis. Donec facilisis pharetra tortor. In nec
mauris eget magna consequat convallis. Nam cras vitae mi vitae odio
pellentesque interdum. Sed consequat viverra nisl. Suspendisse arcu
metus, blandit quis, rhoncus ac, pharetra eget, velit. Mauris
urna. Morbi nonummy molestie orci. Praesent nisi elit, fringilla ac,
suscipit non, tristique vel, mauris. Curabitur vel lorem id nisl porta
adipiscing. Duis vulputate tristique enim. Donec quis lectus a justo
imperdiet tempus. Suspendisse eu lectus. In nunc."""

class DiffTestGeneral(DiffTest):
    """Test a fairly large and general set of texts."""
    def testDiffEmpty(self):
        diff = self.inline_merge.diff_make('text', 'text')
        self.assertEquals('', str(diff))
        
        diff = self.inline_merge.diff_make('', '')
        self.assertEquals('', str(diff))
        
        diff = self.inline_merge.diff_make('\n', '\n')
        self.assertEquals('', str(diff))

class MergeTestGeneral(DiffTest):
    """Attempt to merge a large and general set of texts."""
    def testMergeGeneral(self):
        """Diff two texts. Apply the diff to the first text and see if it
        equals the second text.
        """
        diff = self.inline_merge.diff_make(self.text1, self.text2)
        new_text2 = self.inline_merge.diff_apply(self.text1, diff)
        self.assertEquals(self.text2, new_text2)

if __name__ == "__main__":
  unittest.main()
