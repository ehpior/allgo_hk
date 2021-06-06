import redis

rd = redis.StrictRedis(host='1.240.167.231', port=6379, db=0, password='wjdgusrl34', charset="utf-8", decode_responses=True)

hk = int(rd.get('businessDay_state'))
print(hk)

rd.set('businessDay_state', 4)

hk = int(rd.get('businessDay_state'))
print(hk)

rd.close()
