"""
ckdupes utility functions + the accumulated statistics class def'n
"""
from os import getcwd, remove
import sys
from pydblite import Base


def logger(arg_msg):
    """
    Log a message.
    """
    #now = strftime("%Y-%m-%d %H:%M:%S ", localtime())
    print(arg_msg)


def oops(arg_msg):
    """
    Report an error and exit to the O/S.
    Use sprintf-style argument passing.
    """
    logger("\n*** Oops, {}\n".format(arg_msg))
    sys.exit(86)


class Context:

    
    def __init__(self):
        self.my_name = 'ckdupes'
        self.verbose = False
        self.no_recursion = False
        self.silent_skips = False
        self.db = Base('ckdupes_ram.db')
        if self.db.exists():
            remove(self.db.path)
        self.db.create('bytesize', 'checksum', 'path')
        #curdir = getcwd()
        #logger("Context initialization: db path: {}/{}".format(curdir, self.db.path))
        self.db.create_index('bytesize')
        self.total_dirs = 0
        self.total_files = 0
        self.total_dupes = 0
        self.total_skips = 0
        self.total_file_denied = 0
        self.total_file_nil = 0
        self.total_dir_denied = 0


    def __del__(self):
        if self.db.exists():
            remove(self.db.path)


    def get_totals(self):
        return "total_dirs={}, total_files={}, total_dupes={}, total_skips={}"\
               .format(self.total_dirs, self.total_files, self.total_dupes, self.total_dupes)


if __name__ == '__main__':
        
    context = Context()
    print("bytesize=42 exists? :", context.db(bytesize=42))
    context.db.insert(bytesize=42, checksum=86, path='/tmp')
    rec = context.db(bytesize=42)
    print("bytesize=42 exists? :", rec)
    print('[0]:', rec[0]['checksum'])
