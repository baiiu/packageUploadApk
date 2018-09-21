#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,re
import configReader
import apkParser
import requests

##################################################################
print('\n')
print('=============================================')
print('6. 解析Apk获取上传所需信息: packageName,apkPath,iconPath 等')
print('=============================================')
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

packageName,versionCode,versionName,appLable,iconName = apkParser.getAppBaseInfo(apkPath)

iconPathDir = configReader.code_dir + '/app/src/main/res/mipmap-xxhdpi'
for file in os.listdir(iconPathDir):
    if(os.path.basename(file) == iconName):
        iconPath = iconPathDir + '/' + iconName

print('iconPath: ' + iconPath)


print('\n')
print('=============================================')
print('7. 开始上传 icon 和 apk文件')
print('=============================================')

assembleRelease = configReader.assembleRelease
if(assembleRelease):
    api_token = configReader.api_token_release
else:
    api_token = configReader.api_token_debug

formData = {'type':'android','bundle_id':packageName,'api_token':api_token}
response = requests.post('http://api.fir.im/apps', data = formData)
# print(response.text)
data = response.json()
icon = data['cert']['icon']
binary = data['cert']['binary']
# print(icon['key'])
# print(binary['key'])


def uploadIcon(url,key,token,filePath):
    formData={'key':key,'token':token}
    files = {'file':open(filePath,'rb')}
    response = requests.post(url,data=formData,files = files)
    if(response.ok):
        print('icon 上传成功')


def uploadApk(url,key,token,filePath,appLable,versionName,versionCode):
    formData={'key':key,'token':token,'x:name':appLable,'x:version':versionName,'x:build':versionCode}
    files = {'file':open(filePath,'rb')}
    response = requests.post(url,data=formData,files = files)
    if(response.ok):
        print('apk 上传成功')


uploadIcon(icon['upload_url'],icon['key'],icon['token'],iconPath)
uploadApk(binary['upload_url'],binary['key'],binary['token'],apkPath,appLable,versionName,versionCode)


print('\n')
print('\n')
print('\n')
print('开始测试吧~')
print('--------------')




    #
