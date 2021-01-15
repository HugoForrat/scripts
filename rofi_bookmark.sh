#!/bin/bash

function all_bm {
  url=$(cat $HOME/Bookmarks/* | rofi -dmenu -i | awk -F'|' '{print $NF}')
  [ -n "$url" ] && firefox $url
}

function categorized_bm {
  bm_file=$(ls $HOME/Bookmarks | rofi -dmenu -i)
  [ -n "$bm_file" ] && url=$(cat Bookmarks/"$bm_file" | rofi -dmenu | awk -F'|' '{print $NF}')
  [ -n "$url" ] && firefox $url
}

case $1 in
  all)
    all_bm
    ;;
  *)
    categorized_bm
    ;;
esac
