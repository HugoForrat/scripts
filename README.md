# Scripts

Some scripts I wrote.

## Available scripts
- [sccrawler](/sccrawler/)
- [convert_to_uml](/convert_to_uml.py)
 
A quick and *dirty* way to convert a python file to a file that can be read by [PlantUML](http://plantuml.com).
This only parse methods and attribute and doesn't try to search for inheritance etc...
- [A podcast renaming script](/podcast)
 
A script to download podcasts from the Podcast Addict Android application, and to give, to the best of its ability, sensible and UNIX-compatible filenames.
Needs [`exiftool`](https://sno.phy.queensu.ca/~phil/exiftool/), [`unf`](https://github.com/io12/unf), [`simple-mtpfs`](https://github.com/phatina/simple-mtpfs), as well as `(neo)vim` to work. 
Be careful if you wish to use yourself: some file/directory path are hardcoded and you'll probably want to change them.

- [play.sh](/play.sh)

A bash script for video consumption that remembers for you what the next video you want to watch is.
It does so in a file named `.play` and isn't shy about erasing them so be careful if you have files named like this.
It assumes that it is lauched from the directory where the video files and that the videos are sorted in order in which they should be consumed.
For the moment, it will use [`mpv`](https://mpv.io/) to lauch the videos and it assumes that only video files are present but options may be added in the future.
I'll add `xdg-open` support later.

- [longstuff](/longstuff)

A bash one-liner which sends a notification when the command it received finished or failed.
One can alias commands which are typically long to `longstuff cmd`.
