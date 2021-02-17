import json
import logging


class Jsoner:

    def __init__(self, jason_file):
        self.jason_file = jason_file

    def put_user_into_redis(self, user, r):
        jason_file = json.loads(r.hget('TABLE', 'table'))
        jason_file['users'][f'{user}'] = []
        redis_file = json.dumps(jason_file, indent=4)
        r.hset('TABLE', 'table', redis_file)

    def rec_tasks(self, user, text, r):
        jason_file = json.loads(r.hget('TABLE', 'table'))
        jason_file['users'][f'{user}'].append(text)
        print(jason_file)
        redis_str = json.dumps(jason_file, indent=4)
        r.hset('TABLE', 'table', redis_str)

    def get_tasks(self, user, r):
        jason_file = json.loads(r.hget('TABLE', 'table'))
        tasks = jason_file['users'][f'{user}']
        return tasks

    def delete_tasks(self, user, text, r):
        jason_file = json.loads(r.hget('TABLE', 'table'))
        jason_file['users'][f'{user}'].remove(text)
        redis_str = json.dumps(jason_file, indent=4)
        r.hset('TABLE', 'table', redis_str)
        print(jason_file)


class Remember:

    def __init__(self, user):
        self.user = user


print(Remember(None))