class BaseCache:
    def upsert_value(self, key, value, expire_in):
        raise NotImplementedError

    def get_value(self, key):
        raise NotImplementedError


class RedisCacheDAO(BaseCache):
    def __init__(self, redis_connection):
        self._redis_connection = redis_connection

    def upsert_value(self, key, value, expire_in):
        self._redis_connection.set(key, value, ex=expire_in)

    def get_value(self, key):
        return self._redis_connection.get(key)
