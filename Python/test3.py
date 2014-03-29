#!/usr/bin/env python
# encoding=utf-8

import os

key = '~/.ssh/id_rsa'

str_key = key.split('/')
if str_key[0] == '~' :
	str_key[0] = os.path.expanduser('~')

new_key = '/'.join(str_key)
print 'new_key :  ' + new_key