#!/usr/bin/env python

"""
This runs a command on a remote host using SSH. At the prompts enter hostname,
user, password and the command.
"""

import pexpect
import getpass, os

#user: ssh 
#hostssh 
#passwordssh 
#command ssh 
def ssh_command (user, host, password, command):
    """
    This runs a command on the remote host. This could also be done with the
    pxssh class, but this demonstrates what that class does at a simpler level.
    This returns a pexpect.spawn object. This handles the case when you try to
    connect to a new host and ssh asks you if you want to accept the public key
    fingerprint and continue connecting.
    """
    ssh_newkey = 'Are you sure you want to continue connecting'
    #  ssh  spawn .
    child = pexpect.spawn('ssh -l %s %s %s'%(user, host, command))
    i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password: '])
    # .
    if i == 0: # Timeout
        print 'ERROR!'
        print 'SSH could not login. Here is what SSH said:'
        print child.before, child.after
        return None
    #  ssh  public key.
    if i == 1: # SSH does not have the public key. Just accept it.
        child.sendline ('yes')
        child.expect ('password: ')
        i = child.expect([pexpect.TIMEOUT, 'password: '])
        if i == 0: # Timeout
        print 'ERROR!'
        print 'SSH could not login. Here is what SSH said:'
        print child.before, child.after
        return None
    # .
    child.sendline(password)
    return child

def main ():
    #  ssh .
    host = raw_input('Hostname: ')
    #  ssh .
    user = raw_input('User: ')
    #  ssh .
    password = getpass.getpass()
    #  ssh .
    command = raw_input('Enter the command: ')
    child = ssh_command (user, host, password, command)
    #  pexpect.EOF
    child.expect(pexpect.EOF)
    # .
    print child.before

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print str(e)
        traceback.print_exc()
        os._exit(1)
        