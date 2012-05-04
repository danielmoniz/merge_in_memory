import difflib

class InlineMerge:
    """Stores methods for creating and merging diffs stored in variables."""

    def diff_make(self, text1, text2):
        """Returns the unified diff for two strings."""
        text1_lines = text1.splitlines()
        text2_lines = text2.splitlines()
        differ = difflib.Differ()
        diff = difflib.unified_diff(text1_lines, text2_lines, lineterm='')

        return self.diff_to_string(diff)

    def diff_to_string(self, diff):
        output = '\n'.join(list(diff))
        return output

    def diff_apply(self, text, diff_text, reverse=False):
        """Apply a single diff to a text."""
        diff_lines = diff_text.splitlines()
        text_lines = text.splitlines()
        text_patched = text_lines
        # Iterate through diff sections
        i = 0;
        for line in diff_lines:
            i += 1
            if line.startswith('@'):
                old_info, new_info = self.get_info_from_diff_info_line(line)
                i = int(old_info[0]) - 1
            elif line.startswith('---') or line.startswith('+++'):
                pass
            elif line.startswith('-'):
                if not reverse:
                    # Delete the line.
                    del text_patched[i-1]
                    i -= 1
                else:
                    # Add in a new line.
                    line = line[1:]
                    text_patched.insert(i-1, line)
            elif line.startswith('+'):
                if not reverse:
                    # Add in a new line.
                    line = line[1:]
                    text_patched.insert(i-1, line)
                else:
                    # Delete the line.
                    del text_patched[i-1]
                    i -= 1

        text_patched = '\n'.join(text_patched)
        return text_patched

    def diff_apply_bulk(self, text, diff_list, reverse=False):
        """Apply a number of diffs in order. Do this naively initially."""
        if reverse:
            diff_list = diff_list[::-1]
        for diff in diff_list:
            text = self.diff_apply(text, diff, reverse)
        return text

    def get_info_from_diff_info_line(self, line):
        line = line.replace('-', '')
        line = line.replace('+', '')
        line = line.strip('@')
        line = line.strip()
        #print line
        old_info, new_info = line.split(' ')
        old_info = old_info.split(',')
        new_info = new_info.split(',')
        #print line
        return old_info, new_info

    def merge_apply_bulk(self, text, diffs):
        """Apply a number of diffs to a string in bulk."""
        pass

text1 = """a
test
test
test
test
test
show
test
test
This is a test
And another line.
test
test2
test
test
test
test
test
test
new test
new test
new test
"""

text2 = """
test
test
test
test
test
show
test
test
new test
new test 2
This is a test
A changed line.
test
test
test
test
test
test
test
test
new test
new test
new test
"""

"""
merger = InlineMerge()
diff = merger.diff_make(text1, text2)
#print diff
#print '-'*40

new_text = merger.diff_apply(text1, diff)
print "NEW TEXT: " + '-'*30
print new_text
print "NEW (unpatched) TEXT: " + '-'*30
print text2

new_text1 = merger.diff_apply(text2, diff, reverse=True)
print "ORIGINAL TEXT: " + '-'*30
print text1
print "NEW REVERSE PATCHED TEXT: " + '-'*30
print new_text1
"""
