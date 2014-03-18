#!/usr/bin/python

import sys

if len(sys.argv) < 3 or len(sys.argv) > 4:
    print 'Usage: python', sys.argv[0], '[encode | decode] filename [key]'
    exit(1)
if sys.argv[1] not in ('encode', 'decode'):
    print 'Usage: python', sys.argv[0], '[encode | decode] filename [key]'
    exit(1)
