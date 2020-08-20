"""
ckdupes module for walking a directory tree
"""
import os
from os.path import getsize, isdir, isfile, islink, join
from hashlib import sha1
import ckdupes_utilities as util


MAX_CHUNK_SIZE = int(1e6)


def checksum(arg_path):
    '''
    Compute a checksum for the specified file path.
    '''
    file_hash = sha1()
    fd = os.open(arg_path, os.O_RDONLY)
    chunk = []
    while True:
        chunk = os.read(fd, MAX_CHUNK_SIZE)
        if len(chunk) == 0:
            break
        file_hash.update(chunk)
    os.close(fd)
    return file_hash.digest()


def candidate_file(arg_cur_path, arg_context):
    '''
    For the specified candidate file, does it represent a new entry 
    for the RAM DB or have we seen it before?
    
    Definition of a duplicate: byte size and checksum match
    an existing entry..
    '''
    if not os.access(arg_cur_path, os.R_OK):
        arg_context.total_file_denied += 1
        if not arg_context.silent_skips:
            util.logger("*** Skipping file {}, permission denied".format(arg_cur_path))
        return
    fsize = getsize(arg_cur_path)
    if fsize == 0:
        arg_context.total_file_nil += 1
        if not arg_context.silent_skips:
            util.logger("*** Skipping file {}, nil content".format(arg_cur_path))
        return
    rlist = arg_context.db(bytesize=fsize)  
    if len(rlist) == 0:
        # Doesn't yet exist.
        # Create a new database record.
        cksum = checksum(arg_cur_path)
        if arg_context.verbose:
            util.logger("candidate_file: Creating first size entry:\n\t{}-{}-{}"
                        .format(fsize, cksum, arg_cur_path))
        arg_context.db.insert(bytesize=fsize,
                              checksum=cksum,
                              path=arg_cur_path)
        return
    # Found an existing bytesize entry.
    # Do the checksums match?
    cksum = checksum(arg_cur_path)
    if rlist[0]['checksum'] == cksum:
        # DUPLICATE FOUND.
        # Size and checksum match; they have identical file contents.
        arg_context.total_dupes += 1
        util.logger("{}\t-is a duplicate of-\n\t{}"
                    .format(arg_cur_path, rlist[0]['path']))
    else:
        # Size matched but checksum did not; they are different.
        if arg_context.verbose:
            util.logger("candidate_file: Adding a size entry:\n\t{}-{}-{}"
                        .format(fsize, cksum, arg_cur_path))
        arg_context.db.insert(bytesize=fsize,
                              checksum=checksum(arg_cur_path),
                              path=arg_cur_path)


def traverse(arg_dir_tree, arg_context):
    """
    This is the mechanics of the target tree traverse.
    Note that this function is RECURSIVE.
    """
    if arg_context.verbose:
        util.logger("traverse: cur_base={}, {}"
                    .format(arg_dir_tree, arg_context.get_totals()))
    try:
        leaves = os.listdir(arg_dir_tree)
    except PermissionError:
        arg_context.total_dir_denied += 1
        if not arg_context.silent_skips:
            util.logger("*** Skipping directory {}, permission denied".format(arg_dir_tree))
        return
    except EnvironmentError as ex:
        util.oops("traverse: os.listdir {} failed, reason={}"
                  .format(arg_dir_tree, ex.strerror))
    for leaf in leaves:
        cur_path = join(arg_dir_tree, leaf)
        if islink(cur_path):
            ### Skip links
            arg_context.total_skips += 1
            continue
        if isdir(cur_path):
            ### It's a Directory
            ### If not doing recursion, go get next leaf.
            if arg_context.no_recursion:
                continue
            arg_context.total_dirs += 1
            if arg_context.verbose:
                util.logger("Visited baseline directory: {}".format(cur_path))
            ### Traverse.
            traverse(cur_path, arg_context)
        else: # It's a file, not a directory.
            ### Skip this file if it is not a regular file (E.g. links, sockets, devices)
            if not isfile(cur_path):
                arg_context.total_skips += 1
                if arg_context.verbose:
                    util.logger("Skipping file: {}".format(cur_path))
                continue
            arg_context.total_files += 1
            if arg_context.verbose:
                util.logger("Visited file: {}".format(cur_path))
            candidate_file(cur_path, arg_context)


# === Entry point 'execute' called from ckdupes_main.py =======================
def execute(arg_dir_tree, arg_context):

    ### Perform first traverse (recursive).
    traverse(arg_dir_tree, arg_context)
