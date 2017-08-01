# -*- coding: utf-8 -*-
from pytz import utc
from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
import os

from Trump_New_Schedule_Getter import main as PresMain
from QP_SCORE_MAKER import main as QP_Main

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

sched = BlockingScheduler()

q = Queue(connection=conn)

def gather_Pres_schedule():
    print('starting pres')
    q.enqueue(PresMain)

def gather_QP_Score():
    print('QP maker')
    q.enqueue(QP_Main)

sched.add_job(gather_Pres_schedule, 'cron', day_of_week='*', hour=14, minute=31, timezone='US/Eastern')
sched.add_job(gather_QP_Score, 'cron', day_of_week='*', hour=14, minute=41, timezone='US/Eastern')
sched.start()
