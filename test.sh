#!/bin/sh

cd $(dirname "$0")
. ./virtualenv.sh

export PYTHONPATH=$PWD

test "$1" || set -- plugins/*/test_*
for i; do
    python "$i"
done
