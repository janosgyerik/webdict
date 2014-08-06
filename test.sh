#!/bin/sh

cd $(dirname "$0")
. ./virtualenv.sh

export PYTHONPATH=$PWD

test "$1" || set -- dictionary/test_* plugins/*/test_*
for i; do
    python "$i"
done
