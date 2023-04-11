import asyncio
from pydantic import BaseModel

import uvicorn
from fastapi import FastAPI, Query, File, Response, Body, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse, Response

from query import ark_sign
from user import *

app = FastAPI()
limiter = Limiter(key_func=lambda request: request.query_params["c_id"])  # 根据用户id做频率限制,不传c_id会报错
app.state.limiter = limiter
def my_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    response = JSONResponse(
        {"code": 429, "msg": f"您触发了频率限制: {exc.detail}"}, status_code=429
    )
    response = request.app.state.limiter._inject_headers(
        response, request.state.view_rate_limit
    )
    return response
app.add_exception_handler(RateLimitExceeded, my_limit_exceeded_handler)


@app.get("/")
async def index():
    return Response(content="Hello world", media_type="text/plain")


@app.post("/ark_sign")
@limiter.limit("5/second") #频率限制，一个用户一秒最多5次
# @limiter.limit("200/5 minutes") #频率限制，一个用户5分钟最多200次，可以和上面那个叠加使用
async def sign(request: Request, c_id=Query(None), sign=Query(None),charset=Query(None)):
    try:
        #检查参数是否完全
        if charset == None:
            charset="utf-8"
        if c_id is None or sign is None:
            return {"code": -1, "msg": "c_id/sign require"}
        # 检查用户是否存在
        e = await exist_user(c_id)
        if e == 0:
            return {"code": 403, "msg": "unauthorized"}
        # 检查签名
        ark = await request.body()
        ark = ark.decode("utf-8")
        #ark = ark.encode("gb2312")
        #print(ark)
        md5 = sum_md5(ark + get_user_secret(c_id))
        if md5 != sign:
            return {"code": 403, "msg": "哼哼哼,签名错误啦"}
        # 检查是否有违禁词
        if check_word(ark):
            return {"code": 50000, "msg": "服务繁忙"}
        sign_result = await ark_sign(ark)
        # 记录用户签名次数
        await inc_value(c_id)
        return sign_result
    except Exception as e:
        print(str(e))
        return {"code": 500, "msg": "服务器内部错误"}

@app.get("/add_user")
async def addu(mykey=Query(None), c_id=Query(None)):
    if mykey is None:
            return {"code": 403, "msg": "unauthorized"}
    if mykey != "32bhds9f8253bgu9dstf732":
        # 假装成功了
        return {"code": 200, "data": "ok"}
    await add_user(c_id)
    skey = get_user_secret(c_id)
    return {"code": 200, "data": "okk", "c_id": c_id, "secret_key": skey}

@app.get("/del_user")
async def delu(mykey=Query(None), c_id=Query(None)):
    if mykey is None:
            return {"code": 403, "msg": "unauthorized"}
    if mykey != "32bhds9f8253bgu9dstf732":
        # 假装成功了
        return {"code": 200, "data": "ok"}
    await del_user(c_id)
    return {"code": 200, "data": "okk"}

if __name__ == '__main__':
    # main 为py文件名
    # 6668 大部分浏览器的非安全端口,只能用工具调试接口
    # workers=4 4个进程并发运行
    uvicorn.run("main:app", host="0.0.0.0", port=6688,
                log_level="info", workers=4)  # , reload=True
