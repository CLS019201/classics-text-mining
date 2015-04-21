### sanitizer module

class Sanitizer:
    # <self>, List of strings
    # constructs sanitizer class
    def __init__(self, flags):
        self.flags = flags
    # <self>, string, string
    # given an infile, strips lines in infile that don't contain flags,
    # and writes to outfile
    def clean(self, infile, outfile):
        with open (outfile,"w") as wf:
            wf.write("")
        with open (outfile,"a", encoding='utf-8') as wf:
            with open(infile,"r", encoding='utf-8') as rf:
                for line in rf:
                    if any(key in line for key in self.flags):
                        wf.write(line)