#!/bin/bash

# TODO 
# Check if db is locked or not ?

# TODO
# Handle existing bookmark files

# TODO 
# choice for the destination folder

# TODO 
# Better handling the profile folder

function biggest_profile_folder() {
  du -s $HOME/.mozilla/firefox/*default* | sort -n | tail -n 1 | awk '{print $NF}'
}

ff_db=$(biggest_profile_folder)/places.sqlite
dst_dir="$HOME/Bookmarks" # TODO Control dir directory

# Type 1 => Actual links
# Type 2 => Folders
mkdir -p "$dst_dir"

for folder_id in $(sqlite3 "$ff_db" 'select parent from moz_bookmarks where type=1' | sort -u);
do
  name=$(sqlite3 "$ff_db" "select title from moz_bookmarks where id=$folder_id")
  sqlite3 "$ff_db" \
    "select moz_bookmarks.title, url \
    from moz_bookmarks, moz_places \
    where moz_bookmarks.type=1 and moz_bookmarks.parent=$folder_id and moz_bookmarks.fk = moz_places.id" \
    >> "$dst_dir"/"$name"
done
