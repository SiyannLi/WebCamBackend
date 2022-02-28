class Config(object):
    JOBS = [
        # {
        #     'id': 'record',
        #     'func': 'app:record',
        #     'trigger': 'cron',
        #     'hour': '0'
        # },
        {
            'id': 'delete_useless_video',
            'func': 'app:delete_useless_video',
            'trigger': 'cron',
            'hour': '1'
        }
    ]
    SCHEDULER_API_ENABLED = True
