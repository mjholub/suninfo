#!/home/user/bin/suninfo/bin/python3
"""
Copyright 2024 Marcelina Hołub

     This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU Affero General Public License
     as published by the Free Software Foundation,
     either version 3 of the License,
     or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.
    If not, see <https://www.gnu.org/licenses/>.
"""

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
        time_until = (str(sunrise - now)).split(".")[0]
        if pprint:
            print(f": {time_until}")
        else:
            print(time_until)
    elif now < sunset:
        time_until = (str(sunset - now)).split(".")[0]
        if pprint:
            print(f"󰖚: {time_until}")
        else:
            print(time_until)
    else:
        tomorrow = date.today() + timedelta(days=1)
        s_tomorrow = sun(city.observer, date=tomorrow)
        time_until = (str(s_tomorrow['sunrise'] - now)).split(".")[0]
        if pprint:
            print(f"next sunrise in {time_until}")
        else:
            print(time_until)


interval = parse_args().get('interval', 60)
while True:
    calculate_time_until()
    time.sleep(interval)
