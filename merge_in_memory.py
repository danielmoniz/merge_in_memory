import difflib

class Merger:
    """Stores methods for creating and merging diffs stored in variables."""

    def diff_make(self, text1, text2):
        """Returns the unified diff for two strings."""
        text1_lines = self.manual_splitlines(text1)
        text2_lines = self.manual_splitlines(text2)
        differ = difflib.Differ()
        diff = difflib.unified_diff(text1_lines, text2_lines, lineterm='')

        return self.diff_to_string(diff)

    def manual_splitlines(self, text):
        """Since str.splitlines() removes \\r's from the text as well as \\n's
        (in one fell swoop), use a manual method to split up the lines.
        NOTE: If lines are split with something other than \\n, this method
        will not function properly!
        """
        return text.split('\n')


    def diff_to_string(self, diff):
        """Simply takes a generator diff (eg. from difflib) and outputs it as a string."""
        output = '\n'.join(list(diff))
        return output

    def diff_apply(self, text, diff_text, reverse=False):
        """Apply a single diff to a text. If reverse is set, apply it oppositely."""
        diff_lines = self.manual_splitlines(diff_text)
        text_lines = self.manual_splitlines(text)
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
        """Returns the information from a line if it it is a line that provides line info.
        NOTE: This function falls apart if called on any other type of line.
        """
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
