#!/bin/bash

# 1. 获取mapping文件地址
mappingPath="/Users/zhuzhe/Desktop/mapping.txt"
# echo $mappingPath

# 2. 循环读取reference
# reference="com.immomo.molive.connect.m.c.g\$a.a"
# reference="com.immomo.molive.connect.m.c.g.e"
# reference="com.momo.mwservice.c.Z"
# reference="android.widget.ImageView.mContext"
reference=$1
# echo "reference is ${reference}"

# LeaksInfo中确定性规则：类.变量，最后一个绝对是变量
# 3. 获取类名和变量名
className=${reference%.*}
valueName=${reference##*.}
# echo "className is ${className}"
# echo "valueName is ${valueName}"



# 4. 解析类名
echo "grep -w ${className} ${mappingPath} | grep -v '\\$'"
# 字符串包含$符号么，内部类过滤
if [[ $className == *\$* ]]
then
  classNameGrep=`grep -w ${className}: ${mappingPath}`
else
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
else
  echo "===> ${classNameResult}.${valueNameResult}"
fi


































#
