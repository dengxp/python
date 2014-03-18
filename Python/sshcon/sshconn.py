#!/usr/bin/python
#encoding: UTF-8

#################################################################
# script: encode.py
# description: 实现对文件相关加密解密
# version: 0.1 实现对普通文件的加密解密
# usage: python  encode.py [encode | decode] filename [key]
#################################################################
import sys, os, struct

# 加密字符串
def encodeString(str):
    key_index = 0
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

# 解密字符串
def decodeString(str):
    key_index = 0
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

# 检查命令行参数
if len(sys.argv) < 3 or len(sys.argv) > 4:
    print 'Usage: python', sys.argv[0], '[encode | decode] filename [key]'
    exit(1)
if sys.argv[1] not in ('encode', 'decode'):
    print 'Usage: python', sys.argv[0], '[encode | decode] filename [key]'
    exit(1)
# 文件名
filename = sys.argv[2]
if not os.path.isfile(filename):
    print 'File "' + filename + '" is not exsisted'
    print 'Usage: python', sys.argv[0], '[encode | decode] filename [key]'
    exit(1)
# 定义密钥。加密方式：字符串每个字节与密钥对应字节相加后求余
key = 'TESTKEY'
if len(sys.argv) == 4:
    key = sys.argv[3]
key_bytes = bytearray(key)

# 加密或解密
mode = sys.argv[1]

# 加密或解密文件
file_mode_name = filename + '.' + mode
# 执行加密或解密
if mode == 'encode':
    file = open(filename, 'r')
    file_encode = open(file_mode_name, 'w')
    str = file.read()
    str_encode = encodeString(str)
    file_encode.write(str_encode)
    file.close()
    file_encode.close()
elif mode == 'decode':
    file = open(filename, 'r')
    file_decode = open(file_mode_name, 'w')
    str = file.read()
    str_decode = decodeString(str)
    file_decode.write(str_decode)
    file.close()
    file_decode.close()
print 'Succeed to', mode, 'file "' + filename + '", result file is "' + file_mode_name + '"'
