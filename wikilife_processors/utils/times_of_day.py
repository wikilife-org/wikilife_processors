import datetime


def time_of_day(the_time):
    """
    converts string time to datetime and
    returns time of day
    """
    if type(the_time) == datetime.datetime:
        if the_time.hour < 5:
            return "NIGHT"
        elif the_time.hour < 11:
            return "MORNING"
        elif the_time.hour < 13:
            return "MIDDAY"
        elif the_time.hour < 17:
            return "AFTERNOON"
        elif the_time.hour < 21:
            return "EVENING"
        else:
            return "NIGHT"
    
