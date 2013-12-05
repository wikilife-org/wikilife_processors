# coding=utf-8

from wikilife_processors.processors.stats.was.factors.base_factors_model import \
    Factor, WeeklyAvgAvgFactor
from wikilife_processors.tests.base_test import BaseTest
from wikilife_utils.date_utils import DateUtils


TEST_USER_ID = "TEST_WAAV"
TEST_NODE_ID = 1

class WeeklyAvgAvgFactorTests(BaseTest):
    
    _daos = None

    def setUp(self):
        self._daos = self.get_service_builder().build_managers()
        try:
            self._daos.aggregation_profile_vars_dao._collection.drop()
        except: pass
        
    def test_process_value_21_days(self):
        """
        Current weekly sum average
        """
        print "test_process_value_21_days"
        weekly_avg_day_delta = 21
        factor = self._create_factor(weekly_avg_day_delta)
        current_date = DateUtils.get_datetime_utc()
        test_logs, days = self._get_test_logs_21_days()

        assert self._test_factor(factor, test_logs, days, current_date)

    def test_process_value_22_days(self):
        """
        Current weekly sum average
        """
        print "test_process_value_22_days"
        weekly_avg_day_delta = 21
        factor = self._create_factor(weekly_avg_day_delta)
        current_date = DateUtils.get_datetime_utc()
        test_logs, days = self._get_test_logs_22_days()

        assert self._test_factor(factor, test_logs, days, current_date)

    def test_process_value_22_days_missing_second_week(self):
        """
        Current weekly sum average
        """
        print "test_process_value_22_days_missing_second_week"
        weekly_avg_day_delta = 21
        factor = self._create_factor(weekly_avg_day_delta)
        current_date = DateUtils.get_datetime_utc()
        test_logs, days = self._get_test_logs_22_days_missing_second_week()

        assert self._test_factor(factor, test_logs, days, current_date)

    """ helpers """

    def _create_factor(self, weekly_avg_day_delta):
        values = [
            {"id": "0-1", "name": "0 to 1", "min": 0, "max": 1},
            {"id": "2-10", "name": "2 to 10", "min": 2, "max": 10},
            {"id": "11-20", "name": "11 to 20", "min": 11, "max": 20},
            {"id": "gt20", "name": "more than 20", "min": 20, "max": None}
        ]
        weekly_avg_day_delta = 21
        factor = WeeklyAvgAvgFactor(id="test", name="Test", daos=self._daos, value_type=Factor.BUCKET, values=values, day_delta=weekly_avg_day_delta)
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

    def _get_test_logs_21_days(self):
        days = 21
        """
        from random import randint
        
        for i in range(0, days+1):
            for x in range(0, randint(0, 3)):
                print "{'day': %s, 'value': %s, 'expected': 0}," %(i, randint(1, 20))

        """
        test_logs = [
            {'day': 0,  'value': 5,  'expected': 5},
            {'day': 1,  'value': 8,  'expected': (5+8)/2.0},
            {'day': 2,  'value': 12, 'expected': (5+8+12)/3.0},
            {'day': 6,  'value': 11, 'expected': (5+8+12+11)/4.0},
            {'day': 6,  'value': 2,  'expected': (5+8+12+(11+2)/2.0)/4.0},
            
            {'day': 7,  'value': 7,  'expected': (7.875 + 7 )/2.0},
            {'day': 7,  'value': 4,  'expected': (7.875 + (7+4)/2.0 )/2.0},
            {'day': 10, 'value': 16, 'expected': (7.875 + ((7+4)/2.0 + 16)/2.0 )/2.0},
            {'day': 10, 'value': 2,  'expected': (7.875 + ((7+4)/2.0 + (16+2)/2.0)/2.0 )/2.0},
            {'day': 10, 'value': 3,  'expected': (7.875 + ((7+4)/2.0 + (16+2+3)/3.0)/2.0 )/2.0},
            {'day': 11, 'value': 12, 'expected': (7.875 + ((7+4)/2.0 + (16+2+3)/3.0 + 12)/3.0 )/2.0},
            {'day': 12, 'value': 18, 'expected': (7.875 + ((7+4)/2.0 + (16+2+3)/3.0 + 12 + 18)/4.0 )/2.0},
            
            {'day': 14, 'value': 9,  'expected': (7.875 + 10.625 + 9 )/3.0},
            {'day': 15, 'value': 18, 'expected': (7.875 + 10.625 + (9 + 18)/2.0 )/3.0},
            {'day': 15, 'value': 5,  'expected': (7.875 + 10.625 + (9 + (18+5)/2.0 )/2.0 )/3.0},
            {'day': 16, 'value': 14, 'expected': (7.875 + 10.625 + (9 + (18+5)/2.0 + 14)/3.0 )/3.0},
            {'day': 17, 'value': 3,  'expected': (7.875 + 10.625 + (9 + (18+5)/2.0 + 14 + 3)/4.0 )/3.0},
            {'day': 20, 'value': 18, 'expected': (7.875 + 10.625 + (9 + (18+5)/2.0 + 14 + 3 + 18)/5.0 )/3.0}
        ]

        return test_logs, days

    def _get_test_logs_22_days(self):
        days = 22
        
        """
        week 0: days 1-7
        week 1: days 8-14
        week 2: days 15-21
        """
        
        test_logs = [
            {'day': 0,  'value': 5,  'expected': 0},
            
            {'day': 1,  'value': 8,  'expected': 8},
            {'day': 2,  'value': 12, 'expected': (8+12)/2.0},
            {'day': 6,  'value': 11, 'expected': (8+12+11)/3.0},
            {'day': 6,  'value': 2,  'expected': (8+12+(11+2)/2.0)/3.0},
            {'day': 7,  'value': 7,  'expected': (8+12+(11+2)/2.0+7)/4.0},
            
            {'day': 10, 'value': 3,  'expected': ( 8.375 + 3 )/2.0},
            {'day': 11, 'value': 12, 'expected': ( 8.375 + (3+12)/2.0 )/2.0},
            {'day': 14, 'value': 18, 'expected': ( 8.375 + (3+12+18)/3.0 )/2.0},

            {'day': 15, 'value': 18, 'expected': ( 8.375 + 11 + 18 )/3.0},
            {'day': 15, 'value': 5,  'expected': ( 8.375 + 11 + (18+5)/2.0 )/3.0},
            {'day': 17, 'value': 3,  'expected': ( 8.375 + 11 + ((18+5)/2.0+3)/2.0 )/3.0},
            {'day': 20, 'value': 18, 'expected': ( 8.375 + 11 + ((18+5)/2.0+3+18)/3.0 )/3.0},
            {'day': 21, 'value': 15, 'expected': ( 8.375 + 11 + ((18+5)/2.0+3+18+15)/4.0 )/3.0},
            {'day': 21, 'value': 5,  'expected': ( 8.375 + 11 + ((18+5)/2.0+3+18+(15+5)/2.0)/4.0 )/3.0},
            {'day': 21, 'value': 10, 'expected': ( 8.375 + 11 + ((18+5)/2.0+3+18+(15+5+10)/3.0)/4.0 )/3.0}
        ]

        return test_logs, days

    def _get_test_logs_22_days_missing_second_week(self):
        days = 22

        """
        week 0: days 1-7
        week 1: days 8-14
        week 2: days 15-21
        """

        test_logs = [
            {'day': 0,  'value': 5,  'expected': 0},

            {'day': 1,  'value': 8,  'expected': 8},
            {'day': 2,  'value': 12, 'expected': (8+12)/2.0},
            {'day': 6,  'value': 11, 'expected': (8+12+11)/3.0},
            {'day': 6,  'value': 2,  'expected': (8+12+(11+2)/2.0)/3.0},
            {'day': 7,  'value': 7,  'expected': (8+12+(11+2)/2.0+7)/4.0},

            {'day': 15, 'value': 18, 'expected': ( 8.375 + 18 )/2.0},
            {'day': 15, 'value': 5,  'expected': ( 8.375 + (18+5)/2.0 )/2.0},
            {'day': 17, 'value': 3,  'expected': ( 8.375 + ((18+5)/2.0+3)/2.0 )/2.0},
            {'day': 20, 'value': 18, 'expected': ( 8.375 + ((18+5)/2.0+3+18)/3.0 )/2.0},
            {'day': 21, 'value': 15, 'expected': ( 8.375 + ((18+5)/2.0+3+18+15)/4.0 )/2.0},
            {'day': 21, 'value': 5,  'expected': ( 8.375 + ((18+5)/2.0+3+18+(15+5)/2.0)/4.0 )/2.0},
            {'day': 21, 'value': 10, 'expected': ( 8.375 + ((18+5)/2.0+3+18+(15+5+10)/3.0)/4.0 )/2.0}
        ]

        return test_logs, days
