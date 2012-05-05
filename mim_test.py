import unittest

import merge_in_memory as merge_module

reload(merge_module)

class DiffTest(unittest.TestCase):
    def setUp(self):
        self.inline_merge = merge_module.Merger()
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
        self.assertEquals('', diff)
        
        diff = self.inline_merge.diff_make('', '')
        self.assertEquals('', diff)
        
        diff = self.inline_merge.diff_make('\n', '\n')
        self.assertEquals('', diff)

    def testDiffExistence(self):
        text1 = """first line
second line"""
        text2 = """changed first line
second line"""
        diff = self.inline_merge.diff_make(text1, text2)
        self.assertNotEquals(text1, diff)

        text1 = """first line
second line"""
        text2 = """first line
second line changed"""
        diff = self.inline_merge.diff_make(text1, text2)
        self.assertNotEquals(text1, diff)

        text1 = """first line different
second line"""
        text2 = """first line
second line just as different"""
        diff = self.inline_merge.diff_make(text1, text2)
        self.assertNotEquals(text1, diff)

class MergeTestGeneral(DiffTest):
    """Attempt to merge a large and general set of texts."""
    def testMergeGeneral(self):
        """Diff two texts. Apply the diff to the first text and see if it
        equals the second text.
        """
        diff = self.inline_merge.diff_make(self.text1, self.text2)
        new_text2 = self.inline_merge.diff_apply(self.text1, diff)
        self.assertEquals(self.text2, new_text2)

        new_text2_bulk = self.inline_merge.diff_apply_bulk(self.text1, [diff])
        self.assertEquals(self.text2, new_text2_bulk)

        # And for good measure...
        self.assertEquals(new_text2, new_text2_bulk)

    def testMergeReverseBasic(self):
        text1 = """line 1 here

line 3 here"""
        text2 = """line 1 change here

line 3 here"""
        diff = self.inline_merge.diff_make(text1, text2)
        new_text1 = self.inline_merge.diff_apply(text2, diff, reverse=True)
        self.assertEquals(text1, new_text1)

    def testMergeReverseSpecialChars(self):
        text1 = u'# h1 test #\r\nboldtextisnotbold\r\n\r\nboldtextisnotbold\r\n\r\nChanges #1\r\n\r\nChanges #2'
        text2 = u'# h1 test #\r\nboldtextisnotbold\r\n\r\nboldtextisnotbold\r\n\r\nChanges #1'

        diff = self.inline_merge.diff_make(text1, text2)
        new_text1 = self.inline_merge.diff_apply(text2, diff, reverse=True)
        self.assertEquals(text1, new_text1)

class MergeTestTransitive(DiffTest):
    """Compare composed merges."""
    def testMergeTransitiveBasic(self):
        text1 = """Everything is still."""
        text2 = """Times are changing."""
        text3 = """Times have changed."""

        diff12 = self.inline_merge.diff_make(text1, text2)
        diff23 = self.inline_merge.diff_make(text2, text3)
        diff13 = self.inline_merge.diff_make(text1, text3)

        merge12 = self.inline_merge.diff_apply(text1, diff12)
        merge123 = self.inline_merge.diff_apply(merge12, diff23)

        merge13 = self.inline_merge.diff_apply_bulk(text1, [diff12, diff23])

        self.assertEquals(merge123, merge13)

        # Test reverse bulk merging
        merge31 = self.inline_merge.diff_apply_bulk(merge12, [diff12, diff23], reverse=True)


if __name__ == "__main__":
  unittest.main()
