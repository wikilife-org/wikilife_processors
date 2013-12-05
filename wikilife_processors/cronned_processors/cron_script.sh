#!/bin/sh

#Crontab line
#PROD
#00,30 * *   *   *    /home/tornado/wikilife_backend/wikilife_processors/wikilife_processors/cronned_processors/cron_script.sh prod run /home/tornado/wikilife_backend/wikilife_processors > /dev/null 2>&1

cd $3

export PYTHONPATH=$PYTHONPATH:$PWD;
export PYTHONPATH=$PYTHONPATH:$PWD/../wikilife_utils;
export PYTHONPATH=$PYTHONPATH:$PWD/../wikilife_data;

echo "wikilife_processors Cronned Processors env: $1, cmd: $2";
#nohup python2.7 wikilife_processors/cronned_processors/manage.py $1 "execute" &
python2.7 wikilife_processors/cronned_processors/manage.py $1 "execute"
