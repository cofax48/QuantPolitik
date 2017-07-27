def trigger_execution():
    def Pres():
        from Trump_New_Schedule_Getter import main as PresMain
        print('PresMain Run')
        return 'PresMain Has Run'
    def SecState():
        from sec_state_schedule_quantifier import main as SECMain
        print('SecState Run')
        return 'SecState Has Run'
    def QPMAIN():
        from QP_SCORE_MAKER import main as QP_Main
        print('QP Score Maker Run')
        return 'QPMAIN has run'

    return 'They have all run'
