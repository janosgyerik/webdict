#!/bin/bash -e

cd $(dirname "$0")
. ./virtualenv.sh

test "$1" || set -- plugins/*/test_*.py
for i; do
    i="${i//\//.}"
    i="${i%.py}"
    python -m "$i"
done
