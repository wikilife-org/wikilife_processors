# coding=utf-8

from os import path

#===================================
#   LOGGING CONFIGURATION
#===================================

import logging
LOGGER = logging.getLogger('wikilife_processors')
hdlr = logging.FileHandler(path.join(path.dirname(__file__), "logs/wikilife_processors.log"))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
LOGGER.addHandler(hdlr)
LOGGER.setLevel(logging.INFO)


#===================================
#   PROCESSORS
#===================================

FINAL_LOG_PROCESSOR = "wikilife_processors.processors.logs.final_log_processor.FinalLogProcessor"

"""
PROCESSORS = [
    "wikilife_processors.processors.stats.aggregation_processor.AggregationProcessor", 
    "wikilife_processors.processors.profile.profile_processor.ProfileProcessor"
]
"""
PROCESSORS = [
    "wikilife_processors.processors.stats.aggregation_processor.AggregationProcessor",
    "wikilife_processors.processors.stats.aggregation_node_processor.AggregationNodeProcessor" 
]

DB_SETTINGS = {
    "db_meta_live": {},
    "db_meta_edit": {},
    "db_users": {"name": "wikilife_users"},
    "db_logs": {"name": "wikilife_logs"},
    "db_processors": {"name": "wikilife_processors"},
    "db_crawler": {"name": "wikilife_crawler"},
    "db_apps": {"name": "wikilife_apps"},
    "db_admin": {"name": "wikilife_admin"},
    "db_location": {"name": "geonames"}
}
