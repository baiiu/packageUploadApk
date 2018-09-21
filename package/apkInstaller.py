#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import configReader
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

apk_dir = configReader.apk_dir
code_dir = configReader.code_dir


#6. 安装apk
print('\n')
print('=============================================')
print('install apk')
print('=============================================')


def getFileName(sourceDir):
    if not os.path.exists(sourceDir):
        return;

    for filename in os.listdir(sourceDir):
        if '.apk' in filename:
            return filename


apkName = getFileName(apk_dir)
if(apkName is None or len(apkName) == 0):
    raise Exception("there is no apk to install")

apkPath = apk_dir + '/' + apkName
print('apkPath: '+ apkPath)

os.system('adb install -r ' + apkPath)

#########################################################################################
# 7.打开APK
def cmp(a, b):
    return (a > b) - (a < b)

#获取PackageName,launcherActivity
def findLauncherActivityName(ele,targetString):
    for childElem in ele:
        if len(list(childElem)) == 0:
            if cmp(childElem.get('{http://schemas.android.com/apk/res/android}name'),"'" + targetString +"'"):
                return True
            else:
                return False
        else:
            # print('has child, ' + childElem.tag, childElem.attrib)
            return findLauncherActivityName(childElem,targetString)

def getLauncherActivity(xmlFileDir):
    tree = ET.ElementTree(file=xmlFileDir)

    root = tree.getroot()
    packageName = root.get('package')

    for elem in tree.iter(tag = 'activity'):
        if findLauncherActivityName(elem,'android.intent.action.MAIN'): #if has
            if(findLauncherActivityName(elem,'android.intent.category.LAUNCHER')):
                return packageName,elem.get('{http://schemas.android.com/apk/res/android}name')

    return 'NULL'

PackageName,LauncherActivity = getLauncherActivity(code_dir + '/app/src/main/AndroidManifest.xml')

print (PackageName + '  ' + LauncherActivity)

# PackageName = cf.get('app','PackageName')
# LauncherActivity = cf.get('app','LauncherActivity')

# 先关闭该进程
os.system('adb shell am force-stop ' + PackageName)
# 打开该LauncherActivity
if PackageName in LauncherActivity:
    os.system('adb shell am start -n '+ PackageName +'/' + LauncherActivity)
else:
    os.system('adb shell am start -n '+ PackageName +'/' + PackageName + LauncherActivity)


#
