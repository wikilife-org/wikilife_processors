# coding=utf-8

from wikilife_processors.utils.service_builder import ServiceBuilder
from wikilife_data.utils.db_conn import DBConn
from wikilife_data.utils.dao_builder import DAOBuilder
from wikilife_utils.settings.settings_loader import SettingsLoader
import sys
from wikilife_processors.cronned_processors.profile_agregator import ProfileAgregator

def execute(settings):
    logger = settings["LOGGER"]
    db_user = None
    db_pass = None
    db_conn = DBConn(settings["DB_SETTINGS"], db_user, db_pass)
    dao_builder = DAOBuilder(logger, db_conn)
    service_builder = ServiceBuilder(settings, logger, dao_builder)
    managers = service_builder.build_managers()
    profile_agregator = ProfileAgregator("wikilife_processors.cronned_processors.profile_agregator.ProfileAgregator", logger, managers)
    profile_agregator.execute()

def display_help():
    print "{env} run"


if __name__ == '__main__':
    env = str(sys.argv[1])
    cmd = str(sys.argv[2])
    settings = SettingsLoader().load_settings(env)
    
    if cmd == "execute":
        execute(settings)

    elif cmd == "help":
        display_help()

    else:
        print "Unknown command '%s', use:\n" %cmd
        display_help()
