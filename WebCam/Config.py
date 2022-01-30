class Config(object):
    JOBS = [
        {
            'id': 'record_for_ten_mins',
            'func': 'app:record',
            'trigger': 'interval',
            'seconds': 601
        }
    ]
    SCHEDULER_API_ENABLED = True
