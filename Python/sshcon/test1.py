#!/usr/bin/python
# encoding=utf-8

import pexpect
from sshconlib import *

def ssh_cmd(ip, port, user, passwd) :
	ret = -1
	print 'execute pexpect.spawn'
	
	ssh = pexpect.spawn('ssh -p %s %s@%s' % (port, user, ip))
	
	try :
		i = ssh.expect(['assword:', 'continue connecting (yes/no)?'], timeout = 5)
		if i == 0 :
			ssh.sendline(passwd)
		elif i == 1 :
			ssh.sendline('yes\n')
			ssh.expect('assword: ')
			ssh.sendline(passwd)
			
		r = ssh.read()
		print r
		# pexpect.interact()
		
		ret = 0
	except pexpect.EOF :
		print 'EOF'
		ssh.close()
		ret = -1
		
	except pexpect.TIMEOUT :
		print 'TIMEOUT'
		ssh.close()
		ret = -2
		
	return ret
	
ssh_cmd('42.121.13.207', '22', 'dengxp', '78kxtw!@#')
