'''
ckdupes main program

Usage:	python3   ckdupes_main.py   <TREE>

All duplicates are reported while walking the specified directory tree.

Dependencies:
    numpy
    pydblite (RAM database)

'''
import time
from argparse import ArgumentParser
import ckdupes_utilities as util
import ckdupes_walker


def main(args=None):
    '''
    Main procedure for this module.
    Callable from an external Python program.
    Parameters
        args : list of arguments - mandatory
                The default is None.
    Returns
        None.
    '''

    # Initialialization.
    context = util.Context()
    p = ArgumentParser(prog='python3 {}.py'.format(context.my_name),
                       description='Walk a tree looking for duplicate files.')
    p.add_argument('dir_tree', type=str,
                   help='Directory tree to be walked.')
    p.add_argument('-v', '--verbose', action="store_true", default=False,
                   help='Verbose-execution option')
    p.add_argument('-n', '--no_recursion', action="store_true", default=False,
                   help='Verbose-execution option')
    p.add_argument('-s', '--silent_skips', action="store_true", default=False,
                   help='When skipping a file or directory, do not mention it')
    if args is None:
        args = p.parse_args()
    else:
        args = p.parse_args(args)
    context.verbose = args.verbose
    context.no_recursion = args.no_recursion
    context.silent_skips = args.silent_skips
    
    # Walk directory tree.
    util.logger('Begin')
    time_start = time.time()
    ckdupes_walker.execute(args.dir_tree, context)
    elapsed_time = time.time() - time_start

    # Report findings.
    if elapsed_time > 0.01:
        util.logger('Elapsed seconds = {:.2f}'
                    .format(elapsed_time))
    util.logger('Scanned a total of {} subdirectories and {} files'
                .format(context.total_dirs, context.total_files))
    if context.total_dupes == 0:
        util.logger('No duplicates detected')
    else:
        util.logger('File duplicates: {}'.format(context.total_dupes))
    util.logger('Directory permission issues: {}'.format(context.total_dir_denied))
    util.logger('File permission issues: {}'.format(context.total_file_denied))
    util.logger('Files with nil content: {}'.format(context.total_file_nil))
    util.logger('End')


if __name__ == '__main__':
    main()
