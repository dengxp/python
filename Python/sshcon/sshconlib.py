#!/usr/bin/python
# encoding=utf-8

import sys, os, getpass, struct
			
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
	if str_decode_list[0] <> scfile_header :
		print 'File ' + fn_encode + 'decode Error!'
		return False
		
	fh_decode = open(fn_decode, 'w')
	fh_decode.write(str_decode)
	
	return True
		
		
def rebuild_scfile(scfile, scfile_decode, scfile_header) :
	if check_file_exists(scfile) :
		os.remove(scfile)
		
	h_scfile_decode = open(scfile_decode, 'w')
	h_scfile_decode.write(scfile_header + '\n')
	
	return 0

