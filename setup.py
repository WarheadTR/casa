# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import errno
import traceback

rb_path = os.path.dirname(os.path.realpath(__file__))


def rb_copy(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            print 'Error:', e.args[1]


def casa():
    try:
        casapath = os.environ.get('CASAPATH').split(' ')[0]

        if casapath[-1] == '.':
            count = 0
            for i in range(len(casapath) - 1, -1, -1):
                if casapath[i] == '.':
                    count += 1
                elif casapath[i] == '/':
                    break
            casapath = casapath[:(count*-1)]

        if casapath[-1] == '/':
            pass

        else:
            casapath += '/'

        if os.path.isdir(casapath):
            casa_python = casapath + 'python/2.7/'
            casa_lib = casapath + 'lib/python2.7/'

            if os.path.isdir(casa_python):
                s = rb_path + '/rbindexer/'
                d = casa_python + 'rbindexer/'
                s_test = rb_path + '/tests/test_rbindex.py'
                d_test = casa_python + 'tests/'

                rb_del = 'rm -rf ' + d
                rb_test_del = 'rm -rf ' + d_test + 'test_rbindex.py'

                os.system(rb_del)
                os.system(rb_test_del)

                rb_copy(s, d)
                rb_copy(s_test, d_test)

                print 'Success: rbindexer is ready! You can look README file for usage.'

            elif os.path.isdir(casa_lib):

                s = rb_path + '/rbindexer/'
                d = casa_lib + 'rbindexer/'
                s_test = rb_path + '/tests/test_rbindex.py'
                d_test = casa_lib + 'tests/'

                rb_del = 'rm -rf ' + d
                rb_test_del = 'rm -rf ' + d_test + 'test_rbindex.py'

                os.system(rb_del)
                os.system(rb_test_del)

                rb_copy(s, d)
                rb_copy(s_test, d_test)

                print 'Success: rbindexer is ready! You can look README file for usage.'

        else:
            print traceback.format_exc()
            print "Error: Cannot copy!"


    except:
        print traceback.format_exc()
        print 'Error: Please specify CASAPATH into PATH!'


casa()
