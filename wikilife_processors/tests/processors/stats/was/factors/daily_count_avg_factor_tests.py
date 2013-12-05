# coding=utf-8

from wikilife_processors.processors.stats.was.factors.base_factors_model import \
    Factor, DailyCountAvgFactor
from wikilife_processors.tests.base_test import BaseTest
from wikilife_utils.date_utils import DateUtils


TEST_USER_ID = "TEST_DCAV"
TEST_NODE_ID = 1

class DailyCountAvgFactorTests(BaseTest):
    
    _daos = None

    def setUp(self):
        self._daos = self.get_service_builder().build_managers()
        try:
            self._daos.aggregation_profile_vars_dao._collection.drop()
        except: pass
        
    def test_process_value_f_v_f(self):
        """
        Current daily count average
        first full, some void between, last full
        """
        print "test_process_value_f_v_f"
        daily_avg_day_delta = 7
        factor = self._create_factor(daily_avg_day_delta)
        current_date = DateUtils.get_datetime_utc()
        test_logs, days = self._get_test_logs_f_v_f()

        assert self._test_factor(factor, test_logs, days, current_date)

    def test_process_value_v_v_f(self):
        """
        Current daily count average
        first void, some void between, last full
        """
        print "test_process_value_v_v_f"
        daily_avg_day_delta = 7
        factor = self._create_factor(daily_avg_day_delta)
        current_date = DateUtils.get_datetime_utc()
        test_logs, days = self._get_test_logs_v_v_f()

        assert self._test_factor(factor, test_logs, days, current_date)

    def test_process_value_v_f_v(self):
        """
        Current daily count average
        first void, some full between, last void
        """
        print "test_process_value_v_f_v"
        daily_avg_day_delta = 7
        factor = self._create_factor(daily_avg_day_delta)
        current_date = DateUtils.get_datetime_utc()
        test_logs, days = self._get_test_logs_v_f_v()

        assert self._test_factor(factor, test_logs, days, current_date)

    def test_process_value_few_new_data(self):
        """
        Current daily count average
        """
        print "test_process_value_few_new_data"
        daily_avg_day_delta = 90
        factor = self._create_factor(daily_avg_day_delta)
        current_date = DateUtils.get_datetime_utc()
        test_logs, days = self._get_test_logs_few_new_data()

        assert self._test_factor(factor, test_logs, days, current_date)

    def test_process_value_few_old_data(self):
        """
        Current daily count average
        """
        print "test_process_value_few_old_data"
        daily_avg_day_delta = 90
        factor = self._create_factor(daily_avg_day_delta)
        current_date = DateUtils.get_datetime_utc()
        test_logs, days = self._get_test_logs_few_old_data()

        assert self._test_factor(factor, test_logs, days, current_date)

    """ helpers """

    def _create_factor(self, daily_avg_day_delta):
        values = [
            {"id": "0-1", "name": "0 to 1", "min": 0, "max": 1},
            {"id": "2-10", "name": "2 to 10", "min": 2, "max": 10},
            {"id": "11-20", "name": "11 to 20", "min": 11, "max": 20},
            {"id": "gt20", "name": "more than 20", "min": 20, "max": None}
        ]
        factor = DailyCountAvgFactor(id="test", name="Test", daos=self._daos, value_type=Factor.BUCKET, values=values, day_delta=daily_avg_day_delta)
        return factor

    def _test_factor(self, factor, test_logs, days, current_date):
        success = True

        for log in test_logs:
            raw_value = log["value"]
            exec_date = DateUtils.add_days(current_date, -(days-log["day"]))
            value = factor.process_value(raw_value=raw_value, user_id=TEST_USER_ID, node_id=TEST_NODE_ID, exec_date=exec_date)
            partial_success = round(value, 4) == round(log["expected"], 4)
            print "success: %s, log: %s, processed_value %s" %(partial_success, log, value)
            success = success and partial_success

        print "----\n"

        return success

    def _get_test_logs_f_v_f(self):
        days = 7
        test_logs = [
            {'day': 0,  'value': 5,  'expected': (1)/1.0},
            {'day': 1,  'value': 8,  'expected': (1+1)/2.0},
            {'day': 2,  'value': 12, 'expected': (1+1+1)/3.0},
            {'day': 3,  'value': 7,  'expected': (1+1+1+1)/4.0},
            {'day': 3,  'value': 8,  'expected': (1+1+1+1+1)/4.0},
            {'day': 4,  'value': 9,  'expected': (1+1+1+1+1+1)/5.0},
            {'day': 4,  'value': 1,  'expected': (1+1+1+1+1+1+1)/5.0},
            {'day': 4,  'value': 2,  'expected': (1+1+1+1+1+1+1+1)/5.0},
            {'day': 6,  'value': 3,  'expected': (1+1+1+1+1+1+1+1+1)/6.0},
            {'day': 6,  'value': 2,  'expected': (1+1+1+1+1+1+1+1+1+1)/6.0},
        ]

        return test_logs, days

    def _get_test_logs_v_v_f(self):
        days = 7
        test_logs = [
            {'day': 2,  'value': 12, 'expected': (1)/1.0},
            {'day': 3,  'value': 7,  'expected': (1+1)/2.0},
            {'day': 3,  'value': 8,  'expected': (1+1+1)/2.0},
            {'day': 4,  'value': 9,  'expected': (1+1+1+1)/3.0},
            {'day': 4,  'value': 1,  'expected': (1+1+1+1+1)/3.0},
            {'day': 4,  'value': 2,  'expected': (1+1+1+1+1+1)/3.0},
            {'day': 6,  'value': 3,  'expected': (1+1+1+1+1+1+1)/4.0},
            {'day': 6,  'value': 2,  'expected': (1+1+1+1+1+1+1+1)/4.0}
        ]

        return test_logs, days

    def _get_test_logs_v_f_v(self):
        days = 7
        test_logs = [
            {'day': 2,  'value': 12, 'expected': (1)/1.0},
            {'day': 3,  'value': 7,  'expected': (1+1)/2.0},
            {'day': 3,  'value': 8,  'expected': (1+1+1)/2.0},
            {'day': 4,  'value': 9,  'expected': (1+1+1+1)/3.0},
            {'day': 4,  'value': 1,  'expected': (1+1+1+1+1)/3.0},
            {'day': 4,  'value': 2,  'expected': (1+1+1+1+1+1)/3.0}
        ]

        return test_logs, days

    def _get_test_logs_few_new_data(self):
        days = 7
        test_logs = [
            {'day': 2,  'value': 12, 'expected': (1)/1.0},
            {'day': 3,  'value': 7,  'expected': (1+1)/2.0},
            {'day': 3,  'value': 8,  'expected': (1+1+1)/2.0},
            {'day': 4,  'value': 9,  'expected': (1+1+1+1)/3.0},
            {'day': 4,  'value': 1,  'expected': (1+1+1+1+1)/3.0},
            {'day': 4,  'value': 2,  'expected': (1+1+1+1+1+1)/3.0},
            {'day': 6,  'value': 3,  'expected': (1+1+1+1+1+1+1)/4.0},
            {'day': 6,  'value': 2,  'expected': (1+1+1+1+1+1+1+1)/4.0}
        ]

        return test_logs, days

    def _get_test_logs_few_old_data(self):
        days = 90
        test_logs = [
            {'day': 2,  'value': 12, 'expected': (1)/1.0},
            {'day': 3,  'value': 7,  'expected': (1+1)/2.0},
            {'day': 3,  'value': 8,  'expected': (1+1+1)/2.0},
            {'day': 4,  'value': 9,  'expected': (1+1+1+1)/3.0},
            {'day': 4,  'value': 1,  'expected': (1+1+1+1+1)/3.0},
            {'day': 4,  'value': 2,  'expected': (1+1+1+1+1+1)/3.0},
            {'day': 6,  'value': 3,  'expected': (1+1+1+1+1+1+1)/4.0},
            {'day': 6,  'value': 2,  'expected': (1+1+1+1+1+1+1+1)/4.0}
        ]

        return test_logs, days
