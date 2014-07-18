#!/bin/sh

cd $(dirname "$0")
. ./virtualenv.sh

python application.py
