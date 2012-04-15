from datetime import time


def parse_time(time_string):
    """Parse a GTFS-formatted time into a time and day

    Keyword Arguments:
    time_string -- A 'HH:MM:SS' formatted time

    Return is a tuple:
    time -- a datetime.time
    day -- 0 if the entered time was under 24 hours, 1 if over
    
    If time_string is falsy, (None, None) is returned
    """
    if time_string:
        hour, minute, second = [int(p) for p in time_string.split(':')]
        day = 0
        while hour > 23:
            hour -= 24
            day += 1
        return time(hour, minute, second), day
    return None, None
