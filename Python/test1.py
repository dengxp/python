#!/usr/bin/python
# encoding=utf-8

import sys, os, traceback
import getpass

def check_sc_server_name(server_name) :
	return False
	
def check_sc_ip(ip) :
	return False
	
#######################################################################################################
# 检查IP地址格式是否正确
# 输入参数: IP地址
# 返回值: 检查IP地址是否正确
#######################################################################################################
def check_ip(ip) :
	if not ip :
		return False
	else :
		return True
	
#######################################################################################################
# 检查服务器端口格式是否正确
# 输入参数: 端口号 port
# 返回值: bool
#######################################################################################################
def check_port(port) :
	if str(port).isdigit() and port > 0 or port < 65535 :
		return True
	else :
		return False

#######################################################################################################
# 检查用户名格式是否正确
# 输入参数: 用户名
# 返回值: bool
#######################################################################################################			
def check_user(user_name) :
	if not user_name :
		return False
	else :
		return True
		
def check_public_key(key) :
	
	
	if not key :
		return False
		
	str_key = key.split('/')
	if str_key[0] == '~' :
		str_key[0] = os.path.expanduser(str_key[0])
		new_key = '/'.join(str_key)
	else :
		new_key = key
		
	if os.path.exists(new_key) and os.path.isfile(new_key) :
		return True
	else :
		return False
	
#######################################################################################################
# 从键盘输入服务器名称
# 输入参数: 无
# 返回值: 服务器名称或者False
#######################################################################################################		
def server_name_input() :

	## 输入服务器名称
	server_name = ''
	tries = 0
	isExists = True
	
	# 检查用户输入是否正确，服务器名称是否为空，用户有三次输入机会
	while tries < 3 :
		server_name = raw_input('\n请输入服务器名称: ')
		if not server_name :
			print '您输入的服务器名称为空，请重新输入!'
			tries += 1
		else :
			print '您输入的服务器名称为: ' + server_name
	
			# 检查服务器配置列表中是否已经存在相同的服务器名称
			isExists = check_sc_server_name(server_name)
			if isExists :
				print '\n服务器配置列表中已经存在与[' + server_name + ']同名的服务器配置!'
				while True :
					yes_or_no = raw_input('\n您是否还要继续添加服务器配置 (yes/no) [no] ? ')
					if not yes_or_no :
						yes_or_no = 'no'
						
					if yes_or_no.upper() == 'YES' or yes_or_no.upper() == 'Y' :
						break
					elif yes_or_no.upper() == 'NO' or yes_or_no.upper() == 'N' :
						return False
					else :
						print '请输入[yes/y]或者[no/n]'
			else :
				break
			
	if not server_name and tries >= 3 :
		print '\n您已连续三次输入服务器名称为空，程序退出!'
		print '\n'
		return False
		
	if server_name :
		return server_name
	else :
		return False

#######################################################################################################
# 从键盘输入IP地址
# 输入参数: 无
# 返回值: bool
#######################################################################################################	
def ip_input() :
	ip = ''
	tries = 0
	isExists = True
	result = True
	
	# 检查用户输入是否正确，IP地址是否为空，用户有三次输入机会
	while tries < 3 :
		ip = raw_input('\n请输入IP地址: ')
		
		result = check_ip(ip)
		if not result :
			print '您输入的IP地址为空或者格式错误，请重新输入!'
			tries += 1
		else :
			print '您输入的IP地址为: ' + ip
	
			# 检查服务器配置列表中是否已经存在相同的IP地址
			isExists = check_sc_ip(ip)
			if isExists :
				print '\n服务器配置列表中已经存在与[' + ip + ']相同的IP地址配置!'
				while True :
					yes_or_no = raw_input('\n您是否还要继续添加服务器配置 (yes/no) [no] ? ')
					if not yes_or_no :
						yes_or_no = 'no'
						
					if yes_or_no.upper() == 'YES' or yes_or_no.upper() == 'Y' :
						break
					elif yes_or_no.upper() == 'NO' or yes_or_no.upper() == 'N' :
						return False
					else :
						print '请输入[yes/y]或者[no/n]'
			else :
				break
			
	if not ip and tries >= 3 :
		print '\n您已连续三次输入IP地址为空或者错误，程序退出!'
		print '\n'
		return False
		
	if ip :
		return ip
	else :
		return False
	
#######################################################################################################
# 从键盘输入服务器端口
# 输入参数: 无
# 返回值: bool
#######################################################################################################	
def port_input() :
	port = ''
	tries = 0
	result = True
	
	# 检查用户输入是否正确，IP地址是否为空，用户有三次输入机会
	while tries < 3 :
		port = raw_input('\n请输入服务器端口(回车使用默认端口22): ')
		
		if not port :
			port = '22'
		
		result = check_port(port)
		if not result :
			print '您输入的服务器端口错误，请重新输入!\n'
			print '服务器端口格式要求: '
			print '\t1. 服务器端口为数值.'
			print '\t2. 服务器端口号在区间: [0, 65535].'
			print '\n'
			
			tries += 1
		else :
			print '您输入的服务器端口为: ' + port
			break
			
	if not port and tries >= 3 :
		print '\n您已连续三次输入服务器端口为空或者错误，程序退出!'
		print '\n'
		return False
	
	if port :
		return port
	else :
		return False
			
#######################################################################################################
# 从键盘输入用户名
# 输入参数: 无
# 返回值: bool
#######################################################################################################		
def user_input() :
	user = ''
	tries = 0
	result = True
	
	# 检查用户输入是否正确，用户名是否为空，用户有三次输入机会
	while tries < 3 :
		
		user = raw_input('\n请输入用户名: ')
		
		result = check_user(user)
		if not result :
			print '您输入的用户名为空，请重新输入!\n'			
			tries += 1
		else :
			print '您输入的用户名为: ' + user
			break
			
	if not user and tries >= 3 :
		print '\n您已连续三次输入用户名为空或者错误，程序退出!'
		print '\n'
		return False
		
	return user
		
#######################################################################################################
# 从键盘输入认证方式
# 输入参数: 无
# 返回值: bool
#######################################################################################################		
def auth_type_input() :
	while True :
		auth_type = raw_input('\n请选择认证方式(默认为: 1. 密码认证): \n    1. 密码认证(password)\n    2. 证书认证(public key)\n请选择: ')
		if not auth_type :
			auth_type = 1
	
		print 'auth_type : ' + str(auth_type)
		if int(auth_type) == 1 :
			print '您选择的认证方式为: 1. 密码认证'
			break
		elif int(auth_type) == 2 :
			print '您选择的认证方式为: 2. 证书认证'
			break
		else :
			continue
			
	return auth_type
	
#######################################################################################################
# 从键盘输入用户密码或者私钥文件路径
# 输入参数: 无
# 返回值: bool
#######################################################################################################		
def passwd_or_key_input(auth_type) :
	tries = 0
	result = True
	
	# 检查用户输入是否正确，用户名是否为空，用户有三次输入机会
	while tries < 3 :
		if auth_type == 1 :
			passwd_or_key = getpass.getpass('\n请输入用户密码: ')
			
			if not passwd_or_key :
				print '您输入的密码为空!'
				tries += 1
			else :
				print '您输入的密码为: ' + passwd_or_key
				break
				
		if auth_type == 2 :
			passwd_or_key = raw_input('\n请输入用户私钥文件路径[~/.ssh/id_rsa]: ')
			print '您输入的用户私钥路径为: ' + passwd_or_key
			
			# 处理home目录'~'
		
			result = check_public_key(passwd_or_key)
			if not result :
				print '您输入的用户私钥文件不存在或者不可读，请重新输入!\n'			
				tries += 1
			else :
				print '您输入的用户私钥文件路径为: ' + passwd_or_key
				break
			
	if not passwd_or_key and tries >= 3 :
		if auth_type == 1 :		
			print '\n您已连续三次输入用户密码为空或者错误，程序退出!'
		elif auth_type == 2 :
			print '\n您已连续三次输入用户私钥路径为空或者错误，程序退出!'
			
		print '\n'
		return False
		
	return passwd_or_key

def display_sc_input(server_name, ip, port, user, auth_type, passwd_or_key) :
	print('\n' + ''.ljust(4) + '您输入的信息如下: ')
	print '-'.ljust(72, '-')
	print '\t服务器名称: \t' + server_name
	print '\tIP地址: \t' + ip
	print '\t端口: \t\t' + str(port)
	print '\t用户名: \t' + user
	
	if auth_type == 1 :
		print '\t认证方式: \t1. 密码认证'
		print '\t用户密码: \t' + passwd_or_key
			
	if auth_type == 2 :
		print '\t认证方式: \t2. 证书认证'
		print '\t用户私钥路径: \t' + passwd_or_key
		
	return None
	
def do_add_no_params() :		
	while True :
	
		# 输入服务器名称
		server_name = server_name_input()
		if not server_name :
			return False
			
		# 输入IP地址
		ip = ip_input()
		if not ip :
			return False
			
		# 输入服务器端口
		port = port_input()
		if not port :
			return False
		
		# 输入用户名
		user = user_input()
		if not user :
			return False
			
		# 选择服务器认证方式：1. 密码认证，2. 证书认证
		auth_type = auth_type_input()	
		if not auth_type :
			return False
			
		# 输入用户密码或者用户私钥路径			
		passwd_or_key = passwd_or_key_input(auth_type)
		if not passwd_or_key :
			return False
		
		# 显示输入的信息，供用户检查
		display_sc_input(server_name, ip, port, user, auth_type, passwd_or_key)
			
		# 确认输入的信息是否正确，如果需要修改则返回用户输入
		
		while True :
			yes_or_no = raw_input('\n以上配置信息是否正确？确认请输入[yes/y]，修改请输入[no/n] ')
		
			if yes_or_no.upper() == 'YES' or yes_or_no.upper() == 'Y' :
				print 'save_sc...'
				#save_sc(server_name, ip, port, user, auth_type, passwd_or_key)
				return True
			elif yes_or_no.upper() == 'NO' or yes_or_no.upper() == 'N' :
				print '\n您选择了重新输入服务器配置信息.'
				break
				
			else :
				continue
				
def do_add_with_params(params) :
	if len(params) <> 6 :
		print '参数错误，程序退出!'
		return False
		
	for param in params :
		print param
		
def usage_do_add() :
	print '\n参数错误，正确调用方法为: \n'
	print '\tscadm add'
	print '\tscadm add server_name ip port user auth_type passwd_or_key'
	print '\tscadm add server_name=xx ip=xx port=xx user=xx auth_type=xx passwd_or_key=xx'
	print '\n'
	
	return None
	
#######################################################################################################
# 添加server conf配置
# 输入参数: 此函数无参数
# 返回值: bool，解密是否成功
#######################################################################################################
def do_add(params) :
	
	if len(params) == 0 :
		do_add_no_params()
		
	elif len(params) == 6 :
		do_add_with_params(params)
		
	else :
		usage_do_add()
		return False
	
			
'''

#######################################################################################################
# 添加server conf配置
# 输入参数: 此函数无参数
# 返回值: bool，解密是否成功
#######################################################################################################
def do_delete(params) :
	print 'call do_add'
	print 'params is: ', params
	print 'exec do_add'
	
#######################################################################################################
# 添加server conf配置
# 输入参数: 此函数无参数
# 返回值: bool，解密是否成功
#######################################################################################################
def do_import(params) :
	print 'call do_add'
	print 'params is: ', params
	print 'exec do_add'
	
#######################################################################################################
# 添加server conf配置
# 输入参数: 此函数无参数
# 返回值: bool，解密是否成功
#######################################################################################################
def do_export(params) :
	print 'call do_add'
	print 'params is: ', params
	print 'exec do_add'
	
#######################################################################################################
# 添加server conf配置
# 输入参数: 此函数无参数
# 返回值: bool，解密是否成功
#######################################################################################################
def do_list(params) :
	print 'call do_add'
	print 'params is: ', params
	print 'exec do_add'
	
#######################################################################################################
# 添加server conf配置
# 输入参数: 此函数无参数
# 返回值: bool，解密是否成功
#######################################################################################################
def do_list(params) :
	print 'call do_add'
	print 'params is: ', params
	print 'exec do_add'
	
'''
	
#######################################################################################################
# main entry
#######################################################################################################

action_input = ''
params = []

if len(sys.argv) > 1 :
	action_input = sys.argv[1]
else :
	print '请输入参数.'
	os._exit(-1)
	
if len(sys.argv) > 2 :
	params = sys.argv[2:]

action_list = []
actions = ['add', 'delete', 'import', 'export', 'list', 'clean']

for action in actions :

	if action_input.upper() == action[0:len(action_input)].upper() :
		action_list.append(action)
			
if len(action_list) > 1 :
	print '您输入的参数无法识别'
	os_exit(-1)
else :
	try :
		exec 'do_' + action_list[0] + '(params)'
	except Exception, e:
		print str(e)
		traceback.print_exec()
		os._exit(1)
	
