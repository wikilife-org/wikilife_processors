# coding=utf-8

#===================================
#   TESTS SETTINGS
#===================================

from settings import *

DB_SETTINGS = {
    "db_meta_live": {},
    "db_meta_edit": {},
    "db_users": {"name": "test_wikilife_users"},
    "db_logs": {"name": "test_wikilife_logs"},
    "db_processors": {"name": "test_wikilife_processors"},
    "db_crawler": {"name": "test_wikilife_crawler"},
    "db_apps": {"name": "test_wikilife_apps"},
    "db_admin": {"name": "test_wikilife_admin"},
    "db_location": {"name": "geonames"}
}

# The following will be used for any DB that does not EXPLICITLY override these values.
DB_SETTINGS_DEFAULT = {
    "host": "localhost",
    "port": 27017,
}

DB_SETTINGS["db_meta_live"]["uri"] = "http://localhost:7474/db/data/"

DB_SETTINGS["db_location"]["port"] = 5432
DB_SETTINGS["db_location"]["user"] = "postgres"
DB_SETTINGS["db_location"]["pass"] = "123456"


QUEUE_LOGS = {"host": "localhost", "port": 5672, "name": "log_queue"}
QUEUE_OPERS = {"host": "localhost", "port": 5672, "name": "oper_queue"}

