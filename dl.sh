#!/bin/bash

# # Read a file formated like
# 
# filename1 URL1
# filename2 URL2
# ...
# filenameN URLN
#
# And curl it

while read -r f; do
	curl "$(awk '{print $2}' <<< "$f")" --output "$(awk '{print $1}' <<< "$f")"
done <"$1"
