def trigger_execution():
    from Trump_New_Schedule_Getter import main as PresMain
    print('PresMain Run')
    from sec_state_schedule_quantifier import main as SECMain
    print('SecState Run')
    from QP_SCORE_MAKER import main as QP_Main
    print('QP Score Maker Run')

trigger_execution()
