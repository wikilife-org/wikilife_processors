#!/bin/sh
export PYTHONPATH=$PYTHONPATH:$PWD;
export PYTHONPATH=$PYTHONPATH:$PWD/../wikilife_utils;
export PYTHONPATH=$PYTHONPATH:$PWD/../wikilife_data;

python2.7 wikilife_processors/manage.py $1 $2 $3 $4
