#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# import shutil
try:
    import configparser
except ImportError:
    import ConfigParser

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


# 保持auto.py 和 auto.config在同一级目录下

curDir = os.path.dirname(__file__)
Auto_Config_Path = os.path.dirname(curDir) + '/package.config'
# Auto_Config_Path = curDir + '/package.config'
# print('--> ' + Auto_Config_Path + ' <---')


try:
    cf = configparser.ConfigParser();
    print('python 3')
except Exception as e:
    cf = ConfigParser.ConfigParser();
    print('python 2')


#替换为绝对路径
cf.read(Auto_Config_Path)


Root_SDK_Dir = cf.get('app','Root_SDK_Dir')
git_clone_address = cf.get('app','git_clone_address')
git_branch_name = cf.get('app','git_branch_name')
assembleRelease = cf.getboolean('app','assembleRelease')

api_token_debug = cf.get('private','api_token_debug')
api_token_release = cf.get('private','api_token_release')

unsigned_apk_path = cf.get('sign','unsigned_apk_path') # 未签名的apk
password = cf.get('sign','password')


# 1.设置目录
base_file_dir = cf.get('dir','base_file_dir')
create_dir_name = cf.get('dir','create_dir_name')
create_code_dir_name = cf.get('dir','create_code_dir_name') #源码路径
create_apk_dir_name = cf.get('dir','create_apk_dir_name') # apk路径
release_channel_dir_name = cf.get('dir','release_channel_dir_name') # 渠道包路径

file_dir = base_file_dir + '/' + create_dir_name    #/Users/baiiu/Desktop/AndroidApp
code_dir = file_dir + '/' + create_code_dir_name      #/Users/baiiu/Desktop/AndroidApp/SourceCode
apk_dir = file_dir + '/' + create_apk_dir_name      #/Users/baiiu/Desktop/AndroidApp/Apk
release_channel_dir = file_dir + '/' + release_channel_dir_name #/Users/baiiu/Desktop/AndroidApp/release


if __name__ == "__main__":
    print(Root_SDK_Dir)
    print(git_clone_address)
    print(git_branch_name)
    print(assembleRelease)

    print(file_dir)
    print(code_dir)
    print(apk_dir)
