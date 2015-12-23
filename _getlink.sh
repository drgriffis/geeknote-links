#!/bin/bash
source config

# get the full path to the input file
targetfile=$(abspath "$1")

cd $DIR
targetlink=`$PYTHON links.py getnum $targetfile`
