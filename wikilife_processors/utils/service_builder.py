# coding=utf-8

from wikilife_processors.internal_processor_controller import \
    InternalProcessorController
from wikilife_processors.internal_processors.user_merge_processor import \
    UserMergeProcessor
from wikilife_processors.processor_controller import ProcessorController
from wikilife_processors.processor_info import ProcessorInfo
from wikilife_processors.processor_initializer import ProcessorInitializer
from wikilife_processors.processors.processor_builder import ProcessorBuilder
from wikilife_processors.utils.ancestors import Ancestors
from wikilife_processors.utils.daos import DAOs
from wikilife_processors.utils.log_preprocessor import LogPreprocessor
from wikilife_utils.queue_consumer import QueueConsumer


class ServiceBuilder(object):

    _settings = None
    _logger = None
    _dao_bldr = None
    _processor_builder = None

    def __init__(self, settings, logger, dao_builder):
        self._settings = settings
        self._logger = logger
        self._dao_bldr = dao_builder

    def build_daos(self):
        daos = DAOs()
        daos.generic_dao = self._dao_bldr.build_generic_dao()
        daos.meta_dao = self._dao_bldr.build_live_meta_dao()
        daos.user_dao = self._dao_bldr.build_user_dao()
        daos.profile_dao = self._dao_bldr.build_profile_dao()
        daos.answer_dao = None #self._dao_bldr.build_answer_dao()
        daos.log_dao = self._dao_bldr.build_log_dao()
        daos.stats_dao = None #self._dao_bldr.build_stats_dao()
        daos.generic_stats_dao = None #self._dao_bldr.build_generic_stats_dao()
        daos.timeline_dao = None #self._dao_bldr.build_timeline_dao()
        daos.reports_dao = None #self._dao_bldr.build_reports_dao()
        daos.daily_stats_dao = None #self._dao_bldr.build_daily_stats_dao()
        daos.generic_daily_stats_dao = None #self._dao_bldr.build_generic_daily_stats_dao()
        daos.final_log_dao = self._dao_bldr.build_final_log_dao()
        daos.user_option_last_log_dao = self._dao_bldr.build_user_option_last_log_dao()
        daos.user_log_stats_dao = None #self._dao_bldr.build_user_log_stats_dao()
        daos.generic_global_stats_dao = None #self._dao_bldr.build_generic_global_log_stats_dao()
        daos.profile_report_dao = None #self._dao_bldr.build_profile_report_dao()
        daos.processor_status_dao = self._dao_bldr.build_processor_status_dao()
        daos.cronned_processor_status_dao = None #self._dao_bldr.build_cronned_processor_status_dao()
        daos.flprc_status_dao = self._dao_bldr.build_final_log_processor_status_dao()
        daos.node_daily_dao = None #self._dao_bldr.build_node_daily_dao()
        daos.exercise_dao = None #self._dao_bldr.build_exercise_dao()
        daos.location_dao = self._dao_bldr.build_location_dao()
        daos.aggregation_dao = self._dao_bldr.build_aggregation_dao()
        return daos

    def _build_processor_builder(self):
        if not self._processor_builder:
            daos = self.build_daos()
            log_preprocessor = self._build_log_preprocessor()
            ancestors = self._build_ancestors()
            self._processor_builder = ProcessorBuilder(self._logger, daos, log_preprocessor, ancestors)

        return self._processor_builder

    def _build_log_preprocessor(self):
        meta_dao = self._dao_bldr.build_live_meta_dao()
        return LogPreprocessor(meta_dao)

    def _build_ancestors(self):
        meta_dao = self._dao_bldr.build_live_meta_dao()
        return Ancestors(meta_dao)

    def build_processor_controller(self):
        flprc_class_fullname = self._settings["FINAL_LOG_PROCESSOR"]
        prc_class_fullname_list = self._settings["PROCESSORS"]
        prc_status_dao = self._dao_bldr.build_processor_status_dao()
        flprc_status_dao = self._dao_bldr.build_final_log_processor_status_dao()
        prc_builder = self._build_processor_builder()
        queue_consumer = QueueConsumer(self._logger, self._settings["QUEUE_LOGS"])
        return ProcessorController(self._logger, flprc_class_fullname, prc_class_fullname_list, prc_status_dao, flprc_status_dao, prc_builder, queue_consumer)

    def build_internal_processor_controller(self):
        queue_consumer = QueueConsumer(self._logger, self._settings["QUEUE_OPERS"])
    
        #TODO move this out
        prc_bldr = self._build_processor_builder()
        user_prcs = prc_bldr.build_processor_list(["wikilife_processors.processors.timeline.timeline_processor.TimelineProcessor",
        "wikilife_processors.processors.stats.mood_processor.MoodProcessor",
        "wikilife_processors.processors.stats.meds_processor.MedsProcessor",
        "wikilife_processors.processors.stats.food_processor.FoodProcessor",
        "wikilife_processors.processors.stats.complaint_processor.ComplaintProcessor",
        "wikilife_processors.processors.stats.log_category_processor.LogCategoryProcessor",
        "wikilife_processors.processors.stats.user_log_processor.UserLogProcessor"])
        oper_prc_map = {}
        oper_prc_map["user_merge"] = UserMergeProcessor(user_prcs)

        return InternalProcessorController(self._logger, queue_consumer, oper_prc_map)

    def build_processor_initializer(self):
        flprc_class_fullname = self._settings["FINAL_LOG_PROCESSOR"]
        prc_builder = self._build_processor_builder()
        return ProcessorInitializer(self._logger, flprc_class_fullname, prc_builder)

    def build_processor_info(self):
        flprc_class_fullname = self._settings["FINAL_LOG_PROCESSOR"]
        log_dao = self._dao_bldr.build_log_dao()
        final_log_dao = self._dao_bldr.build_final_log_dao()
        prc_status_dao = self._dao_bldr.build_processor_status_dao()
        flprc_status_dao = self._dao_bldr.build_final_log_processor_status_dao()
        return ProcessorInfo(self._logger, flprc_class_fullname, log_dao, final_log_dao, prc_status_dao, flprc_status_dao)
