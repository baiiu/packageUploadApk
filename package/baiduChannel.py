#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import configReader

code_dir = configReader.code_dir

os.chdir(code_dir)

tag_branch_name = "6.4.1"
baidu_branch_name = "baidu-6.4"
baidu_new_branch_name = "baidu-6.4.1"

os.system('git checkout --track origin/' + baidu_branch_name)
os.system("git checkout -b " + baidu_new_branch_name)
os.system("git merge --no-ff " + tag_branch_name +" -m 'version update'")
os.system("git status")
# os.system("git push --set-upstream origin " + baidu_new_branch_name)
os.system("./gradlew channelRelease")
