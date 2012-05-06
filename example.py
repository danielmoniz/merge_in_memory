import merge_in_memory as mim_module

str1 = """line 1
line 2"""
str2 = """line 1
line 2 changed"""

merger = mim_module.Merger()
diff = merger.diff_make(str1, str2)
print diff
str1_new = merger.diff_apply(str2, diff, reverse=True)
print str1_new
