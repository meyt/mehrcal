#!/bin/sh
SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
if type python2 >/dev/null 2>/dev/null; then
  exec python2 "$SCRIPTPATH/main.py"
else
  echo "Sorry!, This application need python version 2."
fi