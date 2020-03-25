#!/bin/bash

if [ $# != 1 ]
then
	echo "Usage = readMD input_file.md"
	exit
fi

if [ ! ${1: -3} == ".md" ]
then
	echo "The input file must be a markdown (.md) file"
	exit
fi

filename="."$1"-tmp.pdf"

if [ ! -e $filename ] && [ ! -e /tmp/pandoc.tmp ]
then
	pandoc -o $filename $1 2> /tmp/pandoc.tmp
	if [ `wc -c /tmp/pandoc.tmp | sed "s/^\(.\).*$/\1/g"` == 0 ]
	then
		zathura $filename
	else
		echo "Pandoc can't convert the input file."
	fi

	# We erase the buffer files
	rm /tmp/pandoc.tmp
	if [ -e $filename ]
	then
		rm $filename
	fi
else 
	echo "There is an existing file conflicting with my laziness."
fi
