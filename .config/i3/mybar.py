# -*- coding: utf-8 -*-
import asyncio
import json

from datetime import datetime

import sys




def get_message():


    message = [
        {'full_text': ' White Stripes - Seven nation army'},
        {'full_text': ''},
        {'full_text': ''},
        {'full_text': ''},
        {'full_text': ' user'},
        {'full_text': ' battlestation'},
        {
        'full_text': datetime.now().strftime(' %a, %Y-%m-%d %H:%M:%S'),
        'instance': 'asd',
        'markup': 'none',
        'urgent' : False
        }]

    return json.dumps(message)



async def hello_world():
    print('{"version":1}')
    #print(json.dumps({'version': 1, 'click_events': False}))
    print('[')

    print(get_message())
    #print('{}'.format(json.dumps([{'full_text': 'hello_world'}])))
    while True:
        sleep_time = (1000000 - datetime.now().microsecond) / 1000000.0
        await asyncio.sleep(sleep_time)
        sys.stdout.write((',{}\n'.format(get_message())))
        sys.stdout.flush()
        #print(',[{"full_text": "hello_world"}]')

#if __name__ == '__main__':
loop = asyncio.get_event_loop()
loop.run_until_complete(hello_world())
loop.close()
