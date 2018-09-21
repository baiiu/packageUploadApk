#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# sign and rebuild apk
os.system('python3 ' + os.path.dirname(__file__) + '/package/apkSignRebuild.py')
