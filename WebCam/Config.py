class Config(object):
    JOBS = [
        {
            'id': 'record',
            'func': 'app:record',
            'trigger': 'cron',
            'hour': '0'
        }
        # ,
        # {
        #     'id': 'test',
        #     'func': 'app:cron',
        #     'trigger': 'cron',
        #     'second': '*/2'
        # }
    ]
    SCHEDULER_API_ENABLED = True
