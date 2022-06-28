import os
import redis
from metric_name import *


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")
REDIS_PASS = os.getenv("REDIS_PASS")

QUANTITY = "quantity"

red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASS)


class RedisConnection():
    
    def get_metric(self, metric_name):
        metric = red.hgetall(metric_name)
        # {b'rock': b'1', b'pop': b'1'}
        dict_data = {}
        for data in metric:
            # data = "user_id.song"
            total = red.hget(metric_name, data).decode("utf-8")
            split_data = data.decode("utf-8").split(".")
            if len(split_data) == 2:
                user_id = split_data[0]
                multimedia = split_data[1]
                if not user_id in dict_data:
                    dict_data[user_id] = {}
                dict_data[user_id][multimedia] = int(total)
            else: 
                dict_data[data] = int(total)
        return {"metric_name": metric_name,
                "result": dict_data}


    def get_quantity(self, metric_name):
        total = red.hget(metric_name, QUANTITY)
        if not total:
            total = 0
        else:
            total = total.decode("utf-8")
        return {"metric_name": metric_name,
                "result": int(total)}


    def get_all_metrics(self):
        results = []
        metrics = get_quantity_metrics()

        for metric_name in metrics:
            r = self.get_quantity(metric_name)
            results.append(r)
        
        song_metrics = get_song_metrics()
        for metric_name in song_metrics:
            r = self.get_metric(metric_name)
            results.append(r)

        return results
