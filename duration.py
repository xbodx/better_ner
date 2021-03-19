from datetime import datetime, timedelta


def duration(delta: timedelta, interval="default"):
    delta_in_s = delta.total_seconds()

    def __get_duration_in_s(sec=None):
        return sec if sec != None else delta_in_s

    def years():
        return divmod(delta_in_s, 31536000)  # Seconds in a year=31536000.

    def days(sec=None):
        return divmod(__get_duration_in_s(sec), 86400)  # Seconds in a day = 86400

    def hours(sec=None):
        return divmod(__get_duration_in_s(sec), 3600)  # Seconds in an hour = 3600

    def minutes(sec=None):
        return divmod(__get_duration_in_s(sec), 60)  # Seconds in a minute = 60

    def seconds(sec=None):
        return divmod(__get_duration_in_s(sec), 1)

    def millisecond(sec=None):
        return divmod(1000 * __get_duration_in_s(sec), 1)

    def totalDuration(short=True):
        y = years()
        d = days(y[1])
        h = hours(d[1])
        m = minutes(h[1])
        s = seconds(m[1])
        n = millisecond(s[1])
        yi = int(y[0])
        di = int(d[0])
        hi = int(h[0])
        mi = int(m[0])
        si = int(s[0])
        ni = int(n[0])
        s = []
        if yi > 0:
            s.append(f"{yi}" if short else f"{yi} years")
        if di > 0:
            s.append(f"{di}" if short else f"{di}days")
        if hi > 0:
            s.append(f"{hi}" if short else f"{hi} hours")
        if mi > 0:
            s.append(f"{mi}" if short else f"{mi} mins")
        s.append(f"{si}.{ni}" if short else f"{si}.{ni} secs")
        return ' '.join(s)

    return {
        'years': int(years()[0]),
        'days': int(days()[0]),
        'hours': int(hours()[0]),
        'minutes': int(minutes()[0]),
        'seconds': int(seconds()[0]),
        'millisecond': int(millisecond()[0]),
        'long': totalDuration(False),
        'short': totalDuration(True),
        'default': totalDuration(True)
    }[interval]


if __name__ == "__main__":
    start = datetime(2012, 3, 5, 23, 8, 15, 999999)
    finish = datetime(2020, 3, 5, 23, 8, 13, 111111)
    delta = finish - start
    print(duration(delta))
    print(f"years {duration(delta, 'years')}")
    print(f"days {duration(delta, 'days')}")
    print(f"hours {duration(delta, 'hours')}")
    print(f"minutes {duration(delta, 'minutes')}")
    print(f"seconds {duration(delta, 'seconds')}")
    print(f"millisecond {duration(delta, 'millisecond')}")
