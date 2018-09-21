#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,re

def getAppBaseInfo(apkpath):
    os.chdir(os.path.dirname(__file__))

    # 获取版本号等信息
    output = os.popen("./aapt d badging %s" % apkpath).read()

    # package: name='com.baiiu.routerdesignlearn' versionCode='1' versionName='1.0' platformBuildVersionName='7.1.1'
    # package: name='com.baiiu.zhihudaily' versionCode='17122620' versionName='1.4' platformBuildVersionName=''
    matchVersion = re.compile("package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'").match(output)
    if not matchVersion:
        raise Exception("can't get packageinfo")

    packagename = matchVersion.group(1)
    versionCode = matchVersion.group(2)
    versionName = matchVersion.group(3)

    # application: label='RouterDesign' icon='res/mipmap-mdpi-v4/ic_launcher.png'
    outList = output.split('\n')
    for line in outList:
        if line.startswith('application: label'):
            matchName = re.compile("application: label='(\S+)' icon='res/mipmap-mdpi-v4/(\S+)'").match(line)
            if not matchName:
                raise Exception("can't get packageinfo")
            appLable = matchName.group(1)
            iconName = matchName.group(2)
            break


    return packagename,versionCode,versionName,appLable,iconName


def getCurrentDirApk():
    import configReader
    apk_dir = configReader.apk_dir
    def getFileName(sourceDir):
        if not os.path.exists(sourceDir):
            return;

        if not os.listdir(sourceDir):
            return

        for filename in os.listdir(sourceDir):
            if '.apk' in filename:
                return filename

    apkName = getFileName(apk_dir)
    if(apkName is None or len(apkName) == 0):
        raise Exception("there is no apk to upload")

    apkPath = apk_dir + '/' + apkName
    print('apkPath: '+ apkPath)
    return apkPath;

if __name__ == "__main__":
    #获得当前目录下的apk名，用于测试
    apkName = getCurrentDirApk()

    if not apkName:
        print('can not find apk!!!')
        exit()

    os.chdir(os.path.dirname(__file__))
    packagename,versionCode,versionName,appLable,iconName = getAppBaseInfo(apkName)
    print('versionCode: ' + versionCode)
    print('versionName: ' + versionName)
    print('appLable: ' + appLable)
    print('iconName: ' + iconName)
