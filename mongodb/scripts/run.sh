#!/bin/bash
set -m

mongodb_cmd="mongod"
cmd="$mongodb_cmd"

if [ "$AUTH" == "yes" ]; then
    cmd="$cmd --logpath=$MONGODB_LOGPATH --auth"
fi

echo $cmd
$cmd &

if [ ! -f /data/db/.mongodb_password_set ]; then
    $SCRIPT_ROOT/set_password.sh
fi

fg