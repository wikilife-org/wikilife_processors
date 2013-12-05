#!/bin/sh
export PYTHONPATH=$PYTHONPATH:$PWD;
export PYTHONPATH=$PYTHONPATH:$PWD/../wikilife_utils;
export PYTHONPATH=$PYTHONPATH:$PWD/../wikilife_data;

echo "wikilife_processors log_prcs starting ... env=$1";
nohup python2.7 wikilife_processors/manage.py $1 "start_log_prcs" &
echo "Server Started";
