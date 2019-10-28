#!/bin/bash

refResult=

parseRef(){
  # 1. 获取mapping文件地址
  mappingPath="/Users/zhuzhe/Desktop/mapping.txt"
  # echo $mappingPath

  # 2. 循环读取reference
  # reference="com.immomo.molive.connect.m.c.g\$a.a"
  # reference="com.immomo.molive.connect.m.c.g.e"
  # reference="com.momo.mwservice.c.Z"
  # reference="android.widget.ImageView.mContext"
  reference=$1
  echo "reference is ${reference}"

  # LeaksInfo中确定性规则：类.变量，最后一个绝对是变量
  # 3. 获取类名和变量名
  className=${reference%.*}
  valueName=${reference##*.}
  # echo "className is ${className}"
  # echo "valueName is ${valueName}"



  # 4. 解析类名
  # 字符串包含$符号么，内部类过滤
  if [[ $className == *\$* ]]
  then
  echo "grep -w ${className}: ${mappingPath}"
  classNameGrep=`grep -w ${className}: ${mappingPath}`
  else
  echo "grep -w ${className} ${mappingPath} | grep -v '\\$'"
  classNameGrep=`grep -w ${className}: ${mappingPath} | grep -v '\\$'`
  fi

  # echo "${classNameGrep}"
  classNameResult=${classNameGrep% ->*}
  echo "-----> className is ${classNameResult}"


  # 5.解析方法名
  echo "grep -A 100 ${className}: ${mappingPath} | grep -e \"-> ${valueName}\" | head -1"
  valueNameGrep=`grep -A 100 ${className}: ${mappingPath} | grep -e "-> ${valueName}" | head -1`
  # echo ${valueNameGrep}
  valueNameResult=${valueNameGrep% ->*}
  # echo ${valueNameResult}
  valueNameResult=${valueNameResult##* }
  echo "-----> valueName is ${valueNameResult}"


  # 6.还原，替代字符串
  # 类名是否为空，为空则没有匹配上，一是本身没有混淆过；二是解析过程有误，请上报
  if [[ -z ${classNameResult} ]]
  then
  echo "===> ${reference}"
  refResult=${reference}
  else
  echo "===> ${classNameResult}.${valueNameResult}"
  refResult=${classNameResult}.${valueNameResult}
  fi
}

parseFile(){
  IFS=$'\n'
  parseResult=
  for line in `cat $1 | grep -C 2 "* references"`
  do
    # 如果包含GC或references
    if [[ $line == *GC* || $line == *references* ]]
    then
    ref=${line##* }
    echo ${ref}

    parseRef ${ref}
    echo "解析结果: ========>$refResult"

    # 字符串替换，将ref替换成result
    parseResult=$parseResult"\n"${line//$ref/$refResult}
    else
    parseResult=$parseResult"\n"$line
    fi
  done

  echo "parseResult is: \n ${parseResult}"
  if [[ -z ${parseResult} ]]
  then
    # 为空，有点异常
    echo "ERROR"
  else
    echo ${parseResult}"\n\n================================\n\n" >> mmtest.txt
  fi
}

IFS=$'\n\n'
cd $1
for file in `ls $1`
  do
    echo $1"/"$file
    parseFile $1"/"$file
  done
