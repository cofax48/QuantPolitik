# -*- coding: utf-8 -*-
from pytz import utc
from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
import os

from trigger_for_clock import trigger_execution as trigger

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

sched = BlockingScheduler()

q = Queue(connection=conn)

def gather_trigger():
    print('Triggering')
    q.enqueue(trigger)

sched.add_job(gather_trigger, 'cron', day_of_week='*', hour=7, minute=21, timezone='US/Eastern')
sched.start()
