import redis
redis_connect = redis.StrictRedis(charset='utf-8')

l = redis_connect.lrange('menu',0,-1)
for i in l:
    print(str(i))

