# coding=utf-8

from wikilife_processors.processors.base_processor import BaseProcessor
from wikilife_utils.stats_utils import StatsUtils
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.logs.log_nodes import LogNodes

class ExerciseCaloriesBurnedProcessor(BaseProcessor):
    """
    ExerciseProcessor Class

    Processor to manage the exercise information from user logs.

    """

    def accept(self, log):

        try:
            for r in log["nodes"]:
                if "wikilife.exercise.exercise.sport" in r["node_namespace"] and ("calories-burned" in r["node_namespace"] or "duration" in r["node_namespace"] ):
                    return True
            return False
        except Exception, e:
            self._logger.error(e)
            return False


    def insert(self, log):
        """
        Create calories burned information for a user.

        """

        user_id = log["user_id"]
        reports_manager = self._mgrs.reports_mgr
        str_date_hour = str(log["execute_time"]).rstrip("u")
        str_hour = DateUtils.get_time(str_date_hour)
        log_date = DateUtils.get_date(str_date_hour)
        
        nodes_dict_list = LogNodes(log["nodes"]).get_loggables_dict_starting_with("wikilife.exercise.exercise.sport")
        for node_dict in nodes_dict_list:
            info = self._generate_exercise_calories_record(user_id, log["pk"], log_date, str_hour, node_dict)
            
            if info:
                reports_manager.save_exercise_calories_report(info)
        
    def delete(self, log):
        """
        Deletes calories burned information for a user.

        """

        user_id = log["user_id"]
        reports_manager = self._mgrs.reports_mgr
        str_date_hour = str(log["execute_time"]).rstrip("u")
        str_hour = DateUtils.get_time(str_date_hour)
        log_date = DateUtils.get_date(str_date_hour)

        nodes_dict_list = LogNodes(log["nodes"]).get_loggables_dict_starting_with("wikilife.exercise.exercise.sport")
        for node_dict in nodes_dict_list:
            info = {}
            info["log_id"] = int(log["pk"])
            info["user_id"] = user_id
            loggable_ns = log_node_dict.keys()[0]
            info["node_id"] = int(loggable_node["pk"])

            reports_manager.delete_exercise_calories_report(info)
                

    def _generate_exercise_calories_record(self, user_id, log_id, log_date, str_hour, log_node_dict ):

        loggable_ns = log_node_dict.keys()[0]
        loggable_node = self._mgrs.meta_mgr.get_node_by_namespace(loggable_ns)
        
        calories_burned = 0

        properties =  log_node_dict[loggable_ns].keys()
        for property in properties:
            value_key = log_node_dict[loggable_ns][property].keys()[0]
            value = log_node_dict[loggable_ns][property][value_key]["value"]
            if "calories-burned" in property:
                calories_burned = float(value)   
            elif "duration" in property:
                user_profile = self._mgrs.profile_mgr.get_profile_by_user_id(user_id)
                wieght = user_profile["items"]["weight"]
                
                if wieght > 1: 
                    calories_burned = loggable_node["fields"]["calories_burned_factor"] * wieght * float(value)
        
        info = {}
        if calories_burned > 0:
            
            info["log_id"] = int(log_id)
            info["user_id"] = user_id
            info["node_id"] = int(loggable_node["pk"])
            info["date"] = log_date
            info["time"] = str_hour
            info["calories_burned"] = calories_burned
                
        return info
