# coding=utf-8

"""
Load settings
Run command
"""

from wikilife_data.utils.db_conn import DBConn
from wikilife_data.utils.dao_builder import DAOBuilder
from wikilife_processors.utils.service_builder import ServiceBuilder
from wikilife_utils.settings.settings_loader import SettingsLoader
import sys

def start_log_prcs(settings):
    logger = settings["LOGGER"]
    service_builder = _create_service_builder(settings)
    processor_controller = service_builder.build_processor_controller()
    logger.info("ProcessorController instance starting ... environment: %s,  processors: %s" %(settings["ENVIRONMENT"], settings["PROCESSORS"]))
    display_server_info(settings) 
    processor_controller.start()

def start_internal_prcs(settings):
    logger = settings["LOGGER"]
    service_builder = _create_service_builder(settings)
    internal_processor_controller = service_builder.build_internal_processor_controller()
    logger.info("InternalProcessorController instance starting ... environment: %s" %settings["ENVIRONMENT"])
    display_server_info(settings)
    internal_processor_controller.start()

def display_processors(settings):
    service_builder = _create_service_builder(settings)
    prc_info = service_builder.build_processor_info()
    prc_info.print_processor_list()

def display_processor_status(settings, prc_id):
    service_builder = _create_service_builder(settings)
    prc_info = service_builder.build_processor_info()
    prc_info.print_processor_status(prc_id)

def display_final_log_processor_status(settings):
    service_builder = _create_service_builder(settings)
    prc_info = service_builder.build_processor_info()
    prc_info.print_final_log_processor_status()

def initialize_processor(settings, prc_id, days_offset):
    service_builder = _create_service_builder(settings)
    prc_initializer = service_builder.build_processor_initializer()
    prc_initializer.initialize_processor(prc_id, days_offset)

def initialize_final_log_processor(settings, days_offset):
    service_builder = _create_service_builder(settings)
    processor_initializer = service_builder.build_processor_initializer()
    processor_initializer.initialize_final_logs_processor(days_offset)

def display_final_logs_by_month(settings):
    service_builder = _create_service_builder(settings)
    prc_info = service_builder.build_processor_info()
    prc_info.print_final_logs_by_month()

def display_server_info(settings):
    print ""
    print "===== SERVER INFO ====="
    print ""
    print "Server: Wikilife Processors"
    print "Environment: %s" %settings["ENVIRONMENT"]
    print "DB_SETTINGS: %s" %settings["DB_SETTINGS"]
    print ""
    print "======================="
    print ""

def display_help():
    print "{env} runserver : Start processors service \n"
    print "Processor utils:"
    print "================"
    print "{env} list : Display processors list"
    print "{env} status {prc_id} : Display processor status."
    print "{env} statusfl : Display Final Log Processor status"
    print "{env} init {prc_id} {days_offset} : Initialize processor"
    print "{env} initfl {days_offset} : Initialize Final Log Processor"
    print "{env} fl_by_month : Display final logs by month"
    print "\nprc_ids are processors class full name"

def _create_service_builder(settings):
    logger = settings["LOGGER"]
    db_user = None
    db_pass = None
    db_conn = DBConn(settings["DB_SETTINGS"], db_user, db_pass)
    dao_builder = DAOBuilder(logger, db_conn)
    return ServiceBuilder(settings, logger, dao_builder)

if __name__ == "__main__":
    env = str(sys.argv[1])
    cmd = str(sys.argv[2])
    settings = SettingsLoader().load_settings(env)
    
    if cmd == "start_log_prcs":
        start_log_prcs(settings)

    if cmd == "start_internal_prcs":
        start_internal_prcs(settings)

    elif cmd == "list":
        display_processors(settings)

    elif cmd == "status":
        prc_id = str(sys.argv[3])
        display_processor_status(settings, prc_id)

    elif cmd == "statusfl":
        display_final_log_processor_status(settings)

    elif cmd == "init":
        prc_id = str(sys.argv[3])
        days_offset = int(sys.argv[4])
        initialize_processor(settings, prc_id, days_offset)

    elif cmd == "initfl":
        days_offset = int(sys.argv[3])
        initialize_final_log_processor(settings, days_offset)

    elif cmd == "fl_by_month":
        display_final_logs_by_month(settings)

    elif cmd == "help":
        display_help()

    else:
        print "Unknown command '%s', use:\n" %cmd
        display_help()
