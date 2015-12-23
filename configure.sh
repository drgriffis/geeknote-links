#!/usr/bin/env python
import optparse
import os
from subprocess import check_output

def cli():
    parser = optparse.OptionParser(usage='Usage: %prog [OPTIONS]')
    parser.add_option('-p', '--python', dest='python',
            help='path to Python installation to use',
            default=check_output(["which","python"]).strip())
    parser.add_option('-d', '--dir', dest='dir',
            help='path to Geeknote-links directory',
            default=check_output(["pwd"]).strip())
    parser.add_option('-s', '--shell', dest='shell',
            help='shell to execute geeknote-links commands with',
            default=os.environ['SHELL'])
    parser.add_option('-e', '--editor', dest='editor',
            help='editor to use for editing links file',
            default=os.environ['EDITOR'])
    parser.add_option('-g', '--geeknote', dest='geeknote',
            help='path to Geeknote installation to use',
            default=check_output(['which','geeknote']).strip())
    parser.add_option('-m', '--macosx', dest='macosx',
            help='flag for if using OS X (changes some utilities)',
            action='store_true',
            default=False)
    (options, args) = parser.parse_args()
    if False:
        parser.print_help()
        exit()
    return options.python, options.dir, options.shell, options.editor, options.geeknote, options.macosx

if __name__ == '__main__':
    python, gndir, shell, editor, geeknote, macosx = cli()

    if macosx:
        abspath="perl -MCwd -le 'print Cwd::abs_path(shift)'"
    else:
        abspath="readlink -f"

    config = open('config', 'w')
    config.write('#!%s\n' % shell)
    config.write('PYTHON=%s\n' % python)
    config.write('DIR=%s\n' % gndir)
    config.write('GNEDITOR=%s\n' % editor)
    config.write('GEEKNOTE=%s\n' % geeknote)
    config.write('function abspath {\n    echo `%s "$1"`\n}\n' % abspath)
    config.close()
