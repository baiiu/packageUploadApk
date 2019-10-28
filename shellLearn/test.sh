#!/bin/bash

current="Auto-merging .gitignore
CONFLICT (content): Merge conflict in .gitignore
"

# current=`git status`
# echo "$current"

sth(){
  if [[ $current =~ "conflict" ]]
  then
      echo "\n\n\nsth conflict"
      return 0
  fi

  echo "continue"
}

sth
