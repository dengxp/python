#!/usr/bin/python
# encoding=utf-8

import sys, os, getpass, struct
import pexpect

SCFILE_HEADER = '.SERVERS'
SEPARATOR = '\t\t'
			
#######################################################################################################
# 检查密码是否符合要求
#######################################################################################################
def check_password(password) :
	
	if len(password) >= 6:
		return True
	else:
		return False
	
#######################################################################################################
# 检查文件是否存在
#######################################################################################################
def check_file_exists(filename) :
	if os.path.isfile(filename) :
		return True
	else:
		return False

#######################################################################################################
# 检查服务器配置信息是否正确
# 输入参数: 包含服务器配置的list参数
# 返回值: bool
#######################################################################################################
def check_server_properties(properties) :
	
	if len(properties) <> 5 :
		return False
		
	return True


#######################################################################################################
# 加密字符串
# 输入参数: 要加密的字符串
# 返回值: String，加密后的字符串
#######################################################################################################
def encode_string(str, key) :
	if len(key) < 1 :
		print 'The key is null.'
		return -1
		
	key_index = 0
	key_bytes = bytearray(key)
	
	# 定义加密字符串
	str_encode = ''
	
	# 字符串转换成字节数组
	bytes = bytearray(str)
	
	# 按字节加密
	for b in bytes:
		b_encode = (b + key_bytes[key_index]) % 256
		str_encode += struct.pack('B', b_encode)
		key_index = (key_index + 1) % len(key_bytes)
	
	# 返回加密字符串
	return str_encode
		
#######################################################################################################
# 解密字符串
# 输入参数: 要解密的字符串
# 返回值: String，解密后的字符串
#######################################################################################################
def decode_string(str, key) :
	
	if len(key) < 1 :
		print 'The key is null.'
		return -1
				
	key_index = 0
	key_bytes = bytearray(key)
			
	# 定义解密字符串
	str_decode = ''
	# 字符串转换成字节数组
	bytes = bytearray(str)
	for b in bytes:
		b_decode = (b + 256 - key_bytes[key_index]) % 256
		str_decode += struct.pack('B', b_decode)
		key_index = (key_index + 1) % len(key_bytes)
		# 返回解密字符串
	return str_decode

#######################################################################################################
# 加密scfile_decode文件
# 输入参数: fn_decode: 待加密的文件名
# 返回值: bool，解密是否成功
#######################################################################################################

def encode_scfile(fn_decode, fn_encode, key) :
	if not check_file_exists(fn_decode) :
		print 'File ' + fn_decode + 'does not exists!'
		return -1
		
	if len(key) < 1 :
		print 'The key is null.'
		return -2
		
	h_decode = open(fn_decode, 'r')
	h_encode = open(fn_encode, 'w')
	
	str_decode = h_decode.read()
	str_encode = encode_string(str_decode, key)
	h_encode.write(str_encode)
			
#######################################################################################################
# 解密scfile文件
# 输入参数: fn_encode: 待解密的文件名，fn_decode: 解密后的文件名
# 返回值: bool，解密是否成功
#######################################################################################################
def decode_scfile(fn_encode, fn_decode, key) :
	if not check_file_exists(fn_encode) :
		print 'File ' + fn_encode + 'does not exists!'
		return -1
		
	if len(key) < 1 :
		print 'The key is null.'
		return -2
			
	fh_encode = open(fn_encode, 'r')
	str_encode= fh_encode.read()
	str_decode = decode_string(str_encode, key)
	str_decode_list = str_decode.split('\n')

	if str_decode_list[0] <> SCFILE_HEADER :
		print 'File ' + fn_encode + 'decode Error!'
		return False
		
	fh_decode = open(fn_decode, 'w')
	fh_decode.write(str_decode)
	
	return True

#######################################################################################################
# 解密scfile文件, 返回一个list
# 输入参数: fn_encode: 待解密的文件名
# 返回值: list，解密后的list
#######################################################################################################
def decode_scfile_for_list(fn_encode, key) :
	if not check_file_exists(fn_encode) :
		print 'File ' + fn_encode + ' does not exists!'
		return -1
		
	if len(key) < 1 :
		print 'The key is null.'
		return -2

	fh_encode = open(fn_encode, 'r')
	str_encode= fh_encode.read()
	str_decode = decode_string(str_encode, key)
	str_decode_list = str_decode.split('\n')

	if str_decode_list[0] <> SCFILE_HEADER :
		#print 'File ' + fn_encode + ' decode Error!'
		print 'The PASSWORD is error!'
		return False

	for str in str_decode_list :
		if str.count(SEPARATOR) < 4 :
			str_decode_list.remove(str)
			
	return str_decode_list
		
		
def rebuild_scfile(scfile, scfile_decode, SCFILE_HEADER) :
	if check_file_exists(scfile) :
		os.remove(scfile)
		
	h_scfile_decode = open(scfile_decode, 'w')
	h_scfile_decode.write(SCFILE_HEADER + '\n')
	
	return 0
	
#######################################################################################################
# 显示标题
def display_title() :
	print '\n'
	print ' '.ljust(4, ' ') + 'Seq No'.ljust(8, ' ') + 'Server Name'.ljust(28, ' ') + 'IP Address'.ljust(18, ' ') + 'Port'.ljust(10, ' ') + 'User Name'.ljust(16, ' ')
	print '-'.ljust(84, '-')

#######################################################################################################
# 显示服务器配置列表
#######################################################################################################
def display_sc_list(sc_list) :
	# 显示标题
	display_title()

	count = 1

	for sc in sc_list :
		sc_var = sc.split(SEPARATOR)

		del sc_var[len(sc_var) - 1 ]

		if 4 == len(sc_var) :
			print ' '.ljust(4, ' ') + str(count).ljust(8, ' ') +  sc_var[0].ljust(28, ' ') + sc_var[1].ljust(18, ' ') + sc_var[2].ljust(10, ' ') + sc_var[3]

		count += 1

	print '\n'

	return True

#######################################################################################################
# 判断用户输入的是序号、服务器名称还是IP地址
#######################################################################################################
def check_sc_select(server_desc) :
	if server_desc.isdigit() :
		return 1		# means Number, Seq No

	result = 3
	for c in server_desc :
		if c.isdigit() :
			result = 1
			continue
		elif c == '.' :
			result = 2
			break
		else :
			result = 3
			break

	return result

#######################################################################################################
# 连接服务器
#######################################################################################################
def do_connect(server_conf) :
	if len(server_conf) > 1 :
		print '服务器配置信息错误，程序返回'
		return -1
		
	# 把server_conf中的信息填入相关变量
	sc_var = server_conf[0].split(SEPARATOR)
	server_name = sc_var[0]
	host = sc_var[1]
	port = sc_var[2]
	user = sc_var[3]
	passwd = sc_var[4]
	
	# 调用ssh_connect远程连接服务器
	ssh_connect2(host, port, user, passwd)
		
	#docon ip 

#######################################################################################################
# ssh连接服务器
#######################################################################################################

def ssh_connect(host, port, user, passwd) :
	ssh_newkey = 'Are you sure you want to continue connecting'
	ssh = pexpect.spawn('ssh -p %s %s@%s' % (port, user, host))
	i = ssh.expect([pexpect.TIMEOUT, ssh_newkey, 'password: ', '$'])
	print 'i : ', i
	
	# Timeout
	if i == 0 :
		print 'ERROR'
		print 'SSH could not login. Here is what SSH said: '
		print ssh.before, ssh.after
		return None
		
	# ssh public key
	elif i == 1 :
		ssh.sendline('yes')
		ssh.expect('password: ')
		i = ssh.expect([pexpect.TIMEOUT, 'password: '])
		if i == 0 :	# Timeout
			print 'ERROR!'
			print 'SSH could not login. Here is what SSH said: '
			print ssh.before, ssh.after
			return None
			
	elif i == 2 :
		ssh.sendline(passwd)
	
	elif i == 3 :
		print 'Success to login!'
		
	ssh.interact()
		
	return ssh
	
#######################################################################################################
# ssh连接服务器
# ssh_connect2
#######################################################################################################
def ssh_connect2(host, port, user, passwd) :
	ssh_newkey = 'Are you sure you want to continue connecting'
	ssh = pexpect.spawn('ssh -p %s %s@%s' % (port, user, host))
	
	while True :
		i = ssh.expect([pexpect.TIMEOUT, ssh_newkey, 'password: ', '$', '#'])
		
		# Timeout
		if i == 0 :
			print 'ERROR'
			print 'SSH could not login. Here is what SSH said: '
			print ssh.before, ssh.after
			
			break
			
		if i == 1 :
			ssh.sendline('yes')
			continue
		
		if i == 2 :
			ssh.sendline(passwd)
			continue
			
	
		if i == 3 or i == 4 :
			print 'Success to login!'
			break
		
	ssh.interact()
	
	return ssh