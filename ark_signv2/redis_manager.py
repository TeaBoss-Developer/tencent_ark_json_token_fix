from redis import asyncio as aioredis
import asyncio
import os
from config import redis_url, redis_max

# 单例模式（使用装饰器）
def singleton(cls):
    instance = {}

    def wrapper(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return wrapper

@singleton
class RedisManager:
    '''redis连接池'''
    def __init__(self, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self.pool = aioredis.ConnectionPool.from_url(redis_url, max_connections=redis_max)
        self.redis = aioredis.Redis(connection_pool=self.pool)

    async def set_key(self, key, value):
        await self.redis.execute_command("set", key, value)

    async def get_value(self, key):
        value = await self.redis.execute_command("get", key)
        return value
    
    async def exist_key(self, key):
        '''1True,0False'''
        value = await self.redis.execute_command("exists", key)
        return value
    
    async def set_expire(self, key, time):
        await self.redis.execute_command("expire", key, time)

    async def get_expire(self, key):
        value = await self.redis.execute_command("ttl", key)
        return value

    async def exist_hkey(self, key, field):
        '''1True,0False'''
        value = await self.redis.execute_command("hexists", key, field)
        return value
    
    async def set_hkey(self, key, field, value):
        await self.redis.execute_command("hset", key, field, value)

    async def get_hkey(self, key, field):
        value = await self.redis.execute_command("hget", key, field)
        return value

    async def increase_value(self, key):
        # 值自增1
        value = await self.redis.execute_command("incr", key)
        return value

    async def decrease_value(self, key):
        # 值自减1
        value = await self.redis.execute_command("decr", key)
        return value

    async def del_key(self, key):
        await self.redis.execute_command("del", key)
    
    async def del_hkey(self, key, field):
        await self.redis.execute_command("del", key, field)

    def __del__(self):
        self._loop.create_task(self.close())

    async def close(self):
        await self.redis.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
