#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# 1. generate apk
generateApkPath = os.path.dirname(__file__) + '/packageUploadApk/packageAndroid.py'
print(generateApkPath)
os.system('python3 ' + generateApkPath)
