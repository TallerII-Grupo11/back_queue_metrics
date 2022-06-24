import os
import redis


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")
REDIS_PASS = os.getenv("REDIS_PASS")

red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASS)


class RedisConnection():
    
    def get_metric(self, metric_name):
        total = red.hget(metric_name, "quantity")
        if not total:
            total = 0
        else:
            total = total.decode("utf-8")
        return {"metric_name": metric_name,
                "result": int(total)}
    

    def get_all_metrics(self, metrics):
        results = []
        for metric_name in metrics:
            r = self.get_metric(metric_name)
            results.append(r)
        return results
