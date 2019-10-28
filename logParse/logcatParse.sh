#!/bin/bash

parseRef(){
  logcatGrep=`adb logcat -t 10000 | grep -v HttpUtils | grep OkHttp`
  if [[ -z ${logcatGrep} ]]
  then
    return
  fi

  # echo ${logcatGrep}

  if [[ $logcatGrep == *cookie* || $logcatGrep == *User-Agent* ]]
  then
    echo "=======ERROR====="
    echo "=======打印OkHttp日志了=====\n\n"
  fi
}

osascript -e 'tell application "Terminal" to do script "adb logcat | grep OkHttp"'

adb logcat -c

while true
do
    parseRef
    # 每隔1s检测一次
    sleep 1s
done
