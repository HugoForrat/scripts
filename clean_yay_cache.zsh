#!/bin/zsh

if [[ $(pwd) =~ "$HOME/.cache/yay" ]]
then
  # For each directory here
  for f in *(/)
  do
    if ! yay -Qs $f >> /dev/null 
    then
      # echo "Erasing $f"
      rm -rf $f
    fi
  done
else
  echo KO
fi
