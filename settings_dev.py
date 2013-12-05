# coding=utf-8

#===================================
#   DEV ENVIRONMENT SETTINGS
#===================================

from settings import *


# The following will be used for any DB that does not EXPLICITLY override these values.
DB_SETTINGS_DEFAULT = {
    "host": "dev2",
    "port": 27017,
}

DB_SETTINGS["db_meta_live"]["uri"] = "http://dev2:7474/db/data/"

DB_SETTINGS["db_location"]["port"] = 5432
DB_SETTINGS["db_location"]["user"] = "postgres"
DB_SETTINGS["db_location"]["pass"] = "123456"

QUEUE_LOGS = {"host": "localhost", "port": 5672, "name": "dev_log_queue"}
QUEUE_OPERS = {"host": "localhost", "port": 5672, "name": "dev_oper_queue"}
