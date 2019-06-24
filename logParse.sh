#!/bin/bash

parseRef(){
  logcatGrep=`adb logcat -t 10000 | grep -v HttpUtils | grep OkHttp`
  # echo ${logcatGrep}
  if [[ -z ${logcatGrep} ]]
  then
    return
  fi

  if [[ $logcatGrep == *cookie* || $logcatGrep == *User-Agent* ]]
  then
    echo "=======ERROR====="
    echo "=======打印OkHttp日志了====="
  fi
}

while true
do
    parseRef
    adb logcat -c
    sleep 1s
done
