#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,re
import configReader

Root_SDK_Dir = configReader.Root_SDK_Dir
git_clone_address = configReader.git_clone_address
git_branch_name = configReader.git_branch_name
assembleRelease = configReader.assembleRelease

# 1.设置目录
base_file_dir = configReader.base_file_dir
create_dir_name = configReader.create_dir_name
create_code_dir_name = configReader.create_code_dir_name # SourceCode
create_apk_dir_name = configReader.create_apk_dir_name # apk

file_dir = configReader.file_dir    #/Users/baiiu/Desktop/AndroidApp
code_dir = configReader.code_dir      #/Users/baiiu/Desktop/AndroidApp/SourceCode
apk_dir = configReader.apk_dir      #/Users/baiiu/Desktop/AndroidApp/Apk
release_channel_dir = configReader.release_channel_dir

##########################################################################################
#2. 在桌面上创建目录
print ('现在所在位置： ' + os.getcwd())
os.chdir(base_file_dir)
print ('进入桌面： ' + os.getcwd())

print('\n')
print('=============================================')
print('1. create dirs')
print('=============================================')

if not os.path.exists(file_dir):
    os.mkdir(create_dir_name)

os.chdir(file_dir)
print('进入AndroidApp： ' + os.getcwd())

if not os.path.exists(code_dir):
    os.mkdir(create_code_dir_name)

def removeFileInFirstDir(targetDir):#删除一级目录下的所有文件
    for file in os.listdir(targetDir):
        targetFile = os.path.join(targetDir,  file)
        if os.path.isfile(targetFile):
            os.remove(targetFile)
    # os.remove(targetDir)

if(os.path.exists(apk_dir)):
    removeFileInFirstDir(apk_dir)
if(os.path.exists(release_channel_dir)):
    removeFileInFirstDir(release_channel_dir)
    os.rmdir(release_channel_dir)


if not os.path.exists(apk_dir):
    os.mkdir(create_apk_dir_name)

##########################################################################################
#3. 执行git clone命令

# 进入SourceCode目录下
os.chdir(code_dir)
print('进入SourceCode下： ' + os.getcwd())

print('\n')
print('=============================================')
print('2. git command')
print('=============================================')

def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    # return text.strip('* ').strip('\n').strip()
    return text

gitCommandLine = ''

if not os.listdir(code_dir):
    #空文件夹
    gitCommandLine = 'git clone ' + git_clone_address + ' ' + code_dir + ' -b master'
    print(gitCommandLine)
    os.system(gitCommandLine)

#已经clone过,先拉取远端更新
print('\n')
print('git fetch')
os.system('git fetch')


currentBranch = execCmd('git rev-parse --abbrev-ref HEAD')
branches = execCmd('git branch')
if(git_branch_name not in branches):
    gitCommandLine = 'git checkout --track origin/' + git_branch_name
else:
    gitCommandLine = 'git checkout ' + git_branch_name

print('\n')
print('currentBranch: ' + currentBranch.strip('\n'))
print('git_branch_name: '+ git_branch_name)
print('branches: \n'+ branches)

print('\n')
if(len(gitCommandLine) != 0):
    print(gitCommandLine)
    commandLineResult = execCmd(gitCommandLine)
    print('---> '+ commandLineResult.strip('\n') +' <--')
    if(len(commandLineResult)==0):
        raise Exception('the branch is not exist, please check out your config')


# 如果切换本地分支的话拉下代码
print('\n')
print('git pull')
os.system('git pull')



##########################################################################################
#4. gradle assemble打包命令，需要生成local.properties文件

def createLocalPropertiesFile(sourceDir,fileName,root_sdk_dir):
    if not os.path.exists(sourceDir):
        return

    fileDir = sourceDir + '/' + fileName

    if os.path.exists(fileDir):
        return

    f = open(fileDir,'w');
    f.write('sdk.dir=' + root_sdk_dir)
    f.close()

# 生成local.properties文件
createLocalPropertiesFile(code_dir,'local.properties',Root_SDK_Dir)

# 打包
print('\n')
print('=============================================')
print('3. gradle clean')
print('=============================================')
os.system('./gradlew clean')

print('\n')
print('=============================================')
print('4. gradle assemble, generate apk')
print('=============================================')

if(assembleRelease):
    print('assembleRelease apk')
    os.system('./gradlew assembleRelease')
else:
    print('assembleDebug apk')
    os.system('./gradlew assembleDebug')

##########################################################################################
print('\n')
print('=============================================')
print('5. move apk to apkDir')
print('=============================================')
#5.移动.apk文件到Apk目录，方便查找
def moveFiles(sourceDir,  targetDir):#复制一级目录下的所有文件到指定目录
    if not os.path.exists(sourceDir):
        return;

    for file in os.listdir(sourceDir):
         sourceFile = os.path.join(sourceDir,  file)
         targetFile = os.path.join(targetDir,  file)
         # print(sourceFile+ ', ' + targetFile)

         apkFilePath = os.path.basename(sourceFile)
         if os.path.isfile(sourceFile) and ('unaligned' not in apkFilePath) and (apkFilePath.endswith('.apk')):
             open(targetFile,"wb").write(open(sourceFile,"rb").read())


source_apk_dir = code_dir + '/' + 'app/build/outputs/apk'
source_apk_dir += "/release" if assembleRelease else "/debug";
print(source_apk_dir)


if os.path.exists(source_apk_dir):
    moveFiles(source_apk_dir,apk_dir)


#
