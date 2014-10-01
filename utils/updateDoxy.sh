#!/bin/sh
DIR="$( cd "$( dirname "$0" )" && pwd )"
cd "$DIR"
export DG_ROOT="$(dirname "$DIR")"
export DG_VERSION=`cat $PRJ_ROOT/VERSION` 
exec doxygen metaciti.doxyfile

