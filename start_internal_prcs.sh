#!/bin/sh
export PYTHONPATH=$PYTHONPATH:$PWD;
export PYTHONPATH=$PYTHONPATH:$PWD/../wikilife_utils;
export PYTHONPATH=$PYTHONPATH:$PWD/../wikilife_data;

echo "wikilife_processors internal_prcs starting ... env=$1";
nohup python2.7 wikilife_processors/manage.py $1 "start_internal_prcs" &
echo "Server Started";
