#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import configReader

code_dir = '/Users/baiiu/AndroidStudioProjects/work/news'
unsigned_apk_path = configReader.unsigned_apk_path
password = configReader.password

# 1. 签名
line = "apksigner sign --ks " + keystorePath + " --ks-key-alias android.keystore --ks-pass pass:" + password + " --key-pass pass:" + password + " " + unsigned_apk_path


print(line)
os.system(line)

# 2.rebuild channel
os.chdir(os.path.dirname(__file__))
os.system("java -jar ApkChannelPackage.jar get -c " + unsigned_apk_path)
os.system("java -jar ApkChannelPackage.jar put -c sanliuling "+ unsigned_apk_path +"  " + configReader.base_file_dir)
