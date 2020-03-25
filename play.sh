#!/bin/bash

video_cmd="mpv"

if [ -e .play ]
then
	file_to_watch=`cat .play`
	file_found=false
	for f in *
	do
		if [[ $file_found = "true" ]]
		then
			echo $f > .play
			exit 0
		fi

		if [[ $f = $file_to_watch ]]
		then
			$video_cmd $file_to_watch
			file_found=true
		fi
	done
	echo "End of folder."
	echo "Erasing .play"
	rm .play
	exit 0
else
	file_found=false
	for f in *
	do
		if [[ $file_found = "false" ]]
		then
			$video_cmd $f
			file_found=true
		else
			echo $f > .play
			exit 0
		fi
	done
fi
