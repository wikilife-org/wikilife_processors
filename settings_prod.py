# coding=utf-8

#===================================
#   PROD ENVIRONMENT SETTINGS
#===================================

from settings import *


# The following will be used for any DB that does not EXPLICITLY override these values.
DB_SETTINGS_DEFAULT = {
    "host": "db1",
    "port": 27017,
}

DB_SETTINGS["db_meta_live"]["uri"] = "http://db1:7474/db/data/"

DB_SETTINGS["db_location"]["port"] = 5432
DB_SETTINGS["db_location"]["user"] = "postgres"
DB_SETTINGS["db_location"]["pass"] = "123456"


QUEUE_LOGS = {"host": "q1", "port": 5672, "name": "log_queue"}
QUEUE_OPERS = {"host": "q1", "port": 5672, "name": "oper_queue"}