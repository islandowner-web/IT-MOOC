import redis

r = redis.Redis(host='localhost', port=6379, db=0, charset="utf8", decode_responses=True)


r.set("mobile", "123")
r.expire("mobile", 1)#设置过期时间，单位秒
import time
time.sleep(2)
print(r.get("mobile"))