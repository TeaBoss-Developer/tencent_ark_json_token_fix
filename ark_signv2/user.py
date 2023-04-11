# 用户控制 and tools
import hashlib
from config import nwordar
from redis_manager import RedisManager
async def exist_user(key):
    rm = RedisManager()
    return await rm.exist_key("arkuser_" + key)

async def get_user(key):
    rm = RedisManager()
    return await rm.get_value("arkuser_" + key)

async def add_user(key):
    rm = RedisManager()
    await rm.set_key("arkuser_" + key, 0)

async def add_user_expire(key, expire):
    '''添加一个key,并设置key的过期时间(单位:秒)'''
    rm = RedisManager()
    await rm.set_key("arkuser_" + key, 0)
    await rm.set_expire("arkuser_" + key, expire)

async def del_user(key):
    rm = RedisManager()
    await rm.del_key("arkuser_" + key)

async def get_expire(key):
    rm = RedisManager()
    return await rm.get_expire("arkuser_" + key)

async def inc_value(key):
    rm = RedisManager()
    await rm.increase_value("arkuser_" + key)

def check_word(ar):
    for nword in nwordar:
        if nword in ar:
            return True
    return False


def sum_md5(content):  # 计算md5
    md5hash = hashlib.md5(content.encode())
    md5 = md5hash.hexdigest()
    return md5

def get_user_secret(c_id: str) -> str:
    return sum_md5("6Vm4sqwo" + c_id)