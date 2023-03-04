# -*- coding: utf-8 -*-
import asyncio
import json

from datetime import datetime, timedelta
import sys
import os

from getpass import getuser


def user():
    d = {'full_text': ' {}'.format(getuser())}
    return d


from socket import gethostname


def hostname():
    d = {'full_text': ' {}'.format(os.uname()[1])}
    return d


def battery_percentage_to_icon(battery_percentage):
    icons = {0: '\uf244', 1: '\uf243', 2: '\uf242', 3: '\uf241', 4: '\uf240'}
    level = int(battery_percentage / 100.0 * 4 + 0.5)
    return icons[level]


from pathlib import Path


def battery():
    path = Path('/sys/class/power_supply/BAT0/uevent')
    if path.is_file():

        f = path.open()
        battery_text = f.read()
        battery_data = dict(
            [row.split('=') for row in battery_text.strip().splitlines()])

        power_usage = float(battery_data['POWER_SUPPLY_POWER_NOW'])

        if power_usage != 0.0:
            float_hours_left = int(
                battery_data['POWER_SUPPLY_ENERGY_NOW']) / power_usage
        else:
            float_hours_left = 10.0
        hours_left = int(float_hours_left)
        minutes_left = int(float_hours_left * 60) % 60
        percentage = int(battery_data['POWER_SUPPLY_CAPACITY'])

        if battery_data['POWER_SUPPLY_STATUS'] == 'Charging':
            icon = '\uf0e7'
        else:
            icon = battery_percentage_to_icon(percentage)

        d = {
            'full_text':
            '{} {}% {}:{}'.format(icon, percentage, hours_left, minutes_left)
        }
        return d


def metric_time():
    t1 = datetime.now()
    t0 = t1.replace(hour=0, minute=0, second=0, microsecond=0)

    year = t0.replace(month=1, day=1)

    dd = t0 - year

    days = dd.days

    td = t1 - t0

    day = td / timedelta(days=1)

    metric_time = days + day

    d = str(int(day * 10**9))

    s = '{}.{},{}'.format(days, d[0:3], d[3:5])
    

    
    return {'full_text': s}

def get_legacy_time():
    now = datetime.now()
    sleep_time = (1000000 - now.microsecond) / 1000000.0

    return {
            'full_text': now.strftime(' %a, %Y-%m-%d %H:%M:%S'),
            'instance': 'asd',
            'markup': 'none',
            'urgent': False,
            'next_update': (1000000 - datetime.now().microsecond) / 1000000.0
        }


def get_message():

    message = [
        #{'full_text': ' White Stripes - Seven nation army'},
        #{'full_text': ''},
        #{'full_text': ''},
        #{'full_text': ''},
        user(),
        hostname(),
        battery(),
        {
            'full_text': datetime.now().strftime(' %a, %Y-%m-%d %H:%M:%S'),
            'instance': 'asd',
            'markup': 'none',
            'urgent': False
        },
        metric_time()
    ]

    return json.dumps(message)


async def hello_world():
    print('{"version":1}')
    #print(json.dumps({'version': 1, 'click_events': False}))
    print('[')

    print(get_message())
    #print('{}'.format(json.dumps([{'full_text': 'hello_world'}])))
    while True:
        #sleep_time = (1000000 - datetime.now().microsecond) / 1000000.0
        sleep_time = 0.864
        await asyncio.sleep(sleep_time)
        sys.stdout.write((',{}\n'.format(get_message())))
        sys.stdout.flush()
        #print(',[{"full_text": "hello_world"}]')


#if __name__ == '__main__':
loop = asyncio.get_event_loop()
loop.run_until_complete(hello_world())
loop.close()
