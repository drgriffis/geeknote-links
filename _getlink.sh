#!/bin/bash

# get the full path to the input file
targetfile=`readlink -f $1`

cd ~/.scripts/geeknote/links
targetlink=`python links.py getnum $targetfile`
