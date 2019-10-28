#!/bin/bash

# 1. 询问要升级哪个lib，livepushsdk or android_hanisdk#livesdk_foraid，切换到相应目录
# 2. 提示当前version，输入新的version
# 3. 比对，执行uploads
# 4. 切换目录到liveaid，更改相应version，执行clean操作


dir_pushsdk="/Users/zhuzhe/work/livepushsdk"
dir_livesdk="/Users/zhuzhe/work/android_hanisdk"
dir_liveaid="/Users/zhuzhe/work/android_liveaid"


inform() {
    echo "Usage: ./molive.sh [pushsdk|livesdk]"
    echo "pushsdk       means update livepushsdk!"
    echo "livesdk       means update livesdk_foraid, in android_hanisdk!"
    echo "both          means update all"
}

changeDir() {
  if [ $1 == pushsdk ]; then
      cd ${dir_pushsdk}
  elif [ $1 == livesdk ]; then
      cd ${dir_livesdk}
  elif [ $1 == liveaid ]; then
      cd ${dir_liveaid}
  fi

  pwd
}

releaseAid() {
    changeDir "liveaid"


    if [[ $1 == pushsdk ]]; then
      sed -i '' "s/gradle.ext.pushForAid.*$/gradle.ext.pushForAid = false/g" settings.gradle
    elif [[ $1 == livesdk ]]; then
      sed -i '' "s/gradle.ext.haniForAid.*$/gradle.ext.haniForAid = false/g" settings.gradle
    else
      sed -i '' "s/gradle.ext.pushForAid.*$/gradle.ext.pushForAid = false/g" settings.gradle
      sed -i '' "s/gradle.ext.haniForAid.*$/gradle.ext.haniForAid = false/g" settings.gradle
    fi

    ./gradlew clean
    ./gradlew assembleRelease
}

updateAid() {
  changeDir "liveaid"
  pwd

  echo "参数是: $1， $2"

  # 先更改version
  if [[ $1 == pushsdk ]]; then
    sed -i '' "s/pushSdkVersion.*$/pushSdkVersion = \""$2"\"/g" build.gradle
  elif [[ $1 == livesdk ]]; then
    sed -i '' "s/hani_sdk_version.*$/hani_sdk_version = \""$2"\"/g" build.gradle
  fi
}


updatePushsdk() {
  changeDir "pushsdk"
  pwd

  echo "now the pushSDKVersion is: "
  grep -n "\<pushSdkVersion\>" build.gradle

  echo "输入打包版本:"
  read Newversion

  sed -i '' "s/pushSdkVersion.*$/pushSdkVersion = \""${Newversion}"\"/g" build.gradle

  echo "now the pushSdkVersion is: "
  grep -n "\<pushSdkVersion\>" build.gradle

  ./gradlew clean
  ./gradlew uploadarchives

  updateAid "pushsdk" ${Newversion}

  if [[ $1 == "skip" ]]; then
    return 0
  fi

  releaseAid "pushsdk"
}

updateLivesdk() {
  changeDir "livesdk"
  pwd

  # 切换分支
  git status
  git checkout livesdk_foraid

  echo "now the hani_sdk_version is: "
  grep -n "\<hani_sdk_version\>" build.gradle

  echo "输入打包版本:"
  read Newversion

  sed -i '' "s/hani_sdk_version.*$/hani_sdk_version = \""${Newversion}"\"/g" build.gradle

  echo "now the hani_sdk_version is: "
  grep -n "\<hani_sdk_version\>" build.gradle

  ./gradlew clean
  ./gradlew uploadarchives

  updateAid "livesdk" ${Newversion}

  if [[ $1 == "skip" ]]; then
    return 0
  fi

  releaseAid "livesdk"
}

both() {
  updatePushsdk "skip"
  updateLivesdk "skip"

  releaseAid
}


if [[ $1 == pushsdk ]]; then
    updatePushsdk
elif [[ $1 == livesdk ]]; then
    updateLivesdk
elif [[ $1 == both ]]; then
      both
else
    inform
fi
