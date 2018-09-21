#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# 1. generate apk
generateApkPath = os.path.dirname(__file__) + '/package/apkGenerator.py'
os.system('python3 ' + generateApkPath)

# uploadApk
uploadApkPath = os.path.dirname(__file__) + '/package/apkUploader.py'
os.system('python3 ' + uploadApkPath)


# install and open apk
# installApkPath = os.path.dirname(__file__) + '/package/apkInstaller.py'
# os.system('python3 ' + installApkPath)
