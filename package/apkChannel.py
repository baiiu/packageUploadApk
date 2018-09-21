#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# apk渠道包
# https://github.com/ltlovezh/ApkChannelPackage

import configReader
import os


print('\n')
print('=============================================')
print('channel apk')
print('=============================================')


code_dir = configReader.code_dir
os.chdir(code_dir)

print('./gradlew clean')
os.system('./gradlew clean')

print('\n')

print('./gradlew channelRelease')
os.system('./gradlew channelRelease')


def removeFileInFirstDir(targetDir):#删除一级目录下的所有文件
    if not os.path.exists(targetDir):
        return;

    for file in os.listdir(targetDir):
        targetFile = os.path.join(targetDir,  file)
        if os.path.isfile(targetFile):
            os.remove(targetFile)

def moveFiles(sourceDir,  targetDir):#复制一级目录下的所有文件到指定目录
    if not os.path.exists(sourceDir):
        return;
    if not os.path.exists(targetDir):
        os.mkdir(targetDir)

    for file in os.listdir(sourceDir):
         sourceFile = os.path.join(sourceDir,  file)
         targetFile = os.path.join(targetDir,  file)
         print(sourceFile+ ', ' + targetFile)

         apkFilePath = os.path.basename(sourceFile)
         if os.path.isfile(sourceFile) and ('unaligned' not in apkFilePath) and (apkFilePath.endswith('.apk')):
             open(targetFile,"wb").write(open(sourceFile,"rb").read())


release_channel_dir = configReader.release_channel_dir
removeFileInFirstDir(release_channel_dir)

release_apk_dir = code_dir + '/' + 'app/build/channel/release'
print(release_apk_dir)

moveFiles(release_apk_dir,release_channel_dir)
