# -*- coding: utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='*', hour=15, minute=10, timezone='US/Eastern')
def President_Sched():
    from Trump_New_Schedule_Getter import main as PresMain
    PresMain()
    print('PresMain Run')

@sched.scheduled_job('cron', day_of_week='*', hour=15, minute=16, timezone='US/Eastern')
def President_Sched():
    from sec_state_schedule_quantifier import main as SECMain
    SECMain()
    print('SECMain Run')

@sched.scheduled_job('cron', day_of_week='*', hour=15, minute=20, timezone='US/Eastern')
def President_Sched():
    from QP_SCORE_MAKER import main as QP_Main
    QP_Main()
    print('QP Score Maker Run')

sched.start()

if __name__ == '__main__':
    print('starting da trigger')
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        pass
