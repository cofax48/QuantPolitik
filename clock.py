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
    from Trump_New_Schedule_Getter import main as PresMain
    q.enqueue(PresMain)
    print('PresMain Run')
    from sec_state_schedule_quantifier import main as SECMain
    q.enqueue(SECMain)
    print('SecState Run')
    from QP_SCORE_MAKER import main as QP_Main
    q.enqueue(QP_Main)
    print('QP Score Maker Run')

if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(gather_trigger, 'cron', day_of_week='*', hour=15, minute=10, timezone='US/Eastern')

    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        pass
