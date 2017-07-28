# -*- coding: utf-8 -*-
from pytz import utc
from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
import os

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


q = Queue(connection=conn)

def gather_trigger():
    from trigger_for_clock import trigger_execution as trigger
    trigger()
    print('Triggering')
    q.enqueue(trigger)

if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(gather_trigger, 'cron', day_of_week='*', hour=14, minute=22, timezone='US/Eastern')

    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        pass
