#!/usr/bin/python3
import redis

try:
    redis_connect = redis.Redis(host='tzw160702.work', port=6379,
                                decode_responses=True)
    # decode_responses=True 存储的数据是字符串
    redis_connect.set('name', 'zhou')

except Exception as e:
    print(e)

if redis_connect.get('name') == "zhou":
    print("--- redis ok! ---")
