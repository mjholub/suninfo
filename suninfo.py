#!/home/user/bin/suninfo/bin/python3

import time
from argparse import ArgumentParser
from datetime import datetime, date, timedelta
from pytz import timezone


from astral import LocationInfo
from astral.location import Location
from astral.sun import sun


class Result:
    def __init__(self, value=None, error=None):
        self.value = value
        self.error = error

    def is_success(self):
        return self.error is None

    def or_else(self, default):
        return self.value if self.is_success() else default

    def get(self, key, default=None):
        if self.is_success():
            return getattr(self.value, key, default)
        return default


def parse_args():
    try:
        desc = 'Calculate time until sunrise/sunset,'
        parser = ArgumentParser(description=desc)
        parser.add_argument(
            '-p', '--pprint', action='store_true', help="""
            Pretty print the time info instead of returning raw values"""
        )
        parser.add_argument(
            '-i', '--interval', type=int, default=60, help="""
            interval in seconds between updates
            """
        )
        parser.add_argument(
            '-d', '--debug', action='store_true', help="Show debugging info"
        )
        return Result(parser.parse_args())
    except Exception as e:
        return Result(error=str(e))


city = LocationInfo("Kraków", "Poland", "Europe/Warsaw", 50.07, 20.03)

# calculates the time until sunrise or sunset


def calculate_time_until():
    loc = Location(city)
    s = sun(city.observer, date=date.today(), tzinfo=loc.timezone)
    sunrise = s['sunrise']
    sunset = s['sunset']
    now = datetime.now(timezone(city.timezone))
    debug = parse_args().get('debug', False)
    if debug:
        print(f"Sunrise: {sunrise}")
        print(f"Sunset: {sunset}")
        print(f"Now: {now}")

    pprint = parse_args().get('pprint', False)

    if now < sunrise:
        time_until = sunrise - now
        if pprint:
            print(f"Time until sunrise: {time_until}")
        else:
            print(time_until)
    elif now < sunset:
        time_until = sunset - now
        if pprint:
            print(f"Time until sunset: {time_until}")
        else:
            print(time_until)
    else:
        tomorrow = date.today() + timedelta(days=1)
        s_tomorrow = sun(city.observer, date=tomorrow)
        time_until = s_tomorrow['sunrise'] - now
        if pprint:
            print(f"Time until next sunrise: {time_until}")
        else:
            print(time_until)


interval = parse_args().get('interval', 60)
while True:
    calculate_time_until()
    time.sleep(interval)
