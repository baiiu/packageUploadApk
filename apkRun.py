#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,re
import sys
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def buildApk(sourcePath):
    os.chdir(sourcePath)

    print('=============================================')
    print('1. gradle clean')
    print('=============================================')
    os.system('./gradlew clean')

    print('\n')
    print('=============================================')
    print('2. gradle assemble debug, generate apk')
    print('=============================================')
    os.system('./gradlew assembleDebug')

def installApk(sourcePath):
    def getApkPath(rootDir):
        if not os.path.exists(rootDir):
            return;

        for (dirpath, dirnames, filenames) in os.walk(rootDir):
            for filename in filenames:
                if(".apk" in filename):
                    return  os.path.join(dirpath,filename)

    apkPath = getApkPath(sourcePath)
    if(apkPath is None or len(apkPath) == 0):
        raise Exception("there is no apk to install")

    print('=============================================')
    print('3. install apk:' + apkPath)
    print('=============================================')
    os.system('adb install -r ' + apkPath)
    return apkPath

# the applicationId can be changed in gradle, parse the apk is the best way
# def getLauncherActivity(xmlFileDir):
#     def cmp(a, b):
#         return (a > b) - (a < b)
#
#     def findLauncherActivityName(ele,targetString):
#         for childElem in ele:
#             if len(list(childElem)) == 0:
#                 if cmp(childElem.get('{http://schemas.android.com/apk/res/android}name'),"'" + targetString +"'"):
#                     return True
#                 else:
#                     return False
#             else:
#                 # print('has child, ' + childElem.tag, childElem.attrib)
#                 return findLauncherActivityName(childElem,targetString)
#
#     tree = ET.ElementTree(file=xmlFileDir)
#
#     root = tree.getroot()
#     packageName = root.get('package')
#
#     for elem in tree.iter(tag = 'activity'):
#         if findLauncherActivityName(elem,'android.intent.action.MAIN'): #if has
#             if(findLauncherActivityName(elem,'android.intent.category.LAUNCHER')):
#                 return packageName,elem.get('{http://schemas.android.com/apk/res/android}name')
#
#     return 'NULL'

def getLauncherActivity(apkPath):
    print('=============================================')
    print('4. 打开apk:' + apkPath)
    print('=============================================')

    output = os.popen("./package/aapt d badging %s" % apkPath).read()

    # package: name='com.immomo.honeyapp' versionCode='1' versionName='1.0' platformBuildVersionName=''
    matchVersion = re.compile("package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'").match(output)
    packageName = matchVersion.group(1)
    print("packageName: "+packageName)

    # launchable-activity: name='com.example.zhuzhe.momoshare.MainActivity'  label='' icon=''
    matchLaunchar= re.search("launchable-activity: name='(\S+)' ",output)
    launcharAct = matchLaunchar.group(1)
    print("launcharAct: "+launcharAct)


    return packageName,launcharAct


if __name__ == '__main__':
    # 1. 获取打包路径
    sourcePath = sys.argv[1]
    if(len(sourcePath) == 0):
        sourcePath = "/Users/zhuzhe/work/momodev"

    print("sourcePath is " + sourcePath)

    # 2. clean并打包
    buildApk(sourcePath)

    # 3. 安装apk
    apkPath = installApk(sourcePath + "/app/build/outputs/apk")
    if(len(apkPath) == 0):
        raise Exception("no apk")


    # 4. 获取LauncharAct
    packageName,launcherActivity = getLauncherActivity(apkPath)
    print (packageName + '  ' + launcherActivity)
    if(len(packageName) == 0 or len(launcherActivity) == 0):
        raise Exception("no activity run")

    # 先关闭该进程
    os.system('adb shell am force-stop ' + packageName)
    # 打开该launcherActivity
    # if packageName in launcherActivity:
    os.system('adb shell am start -n '+ packageName +'/' + launcherActivity)
    # else:
        # os.system('adb shell am start -n '+ packageName +'/' + packageName + launcherActivity)
