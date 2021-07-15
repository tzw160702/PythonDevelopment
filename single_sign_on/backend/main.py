#! /usr/bin/env python

# coding=UTF-8
from fastapi import status, FastAPI, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import api
import env
from loguru import logger
from datetime import date, timedelta
from aioredis import create_redis_pool
import os

app = FastAPI()

# 注册 APIRouter  路由
app.include_router(api.code_router, tags=["code"], prefix="/code")
app.include_router(api.login_router, tags=["users"], prefix="/users")
app.include_router(api.token_router, tags=["token"], prefix="/token")

# 解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 挂载 redis
def register_redis(app: FastAPI) -> None:
    """
    挂载 redis 到 app 对象上面
    :param app:
    :return:
    """
    @app.on_event("startup")
    async def startup_event():
        """
        获取 redis 链接
        """
        app.state.redis = await create_redis_pool(env.REDIS_URL)

    @app.on_event("shutdown")
    async def shutdown():
        """
        关闭 redis
        """
        app.state.redis.close()
        await app.state.redis.wait_closed()


if __name__ == '__main__':
    import uvicorn
    register_redis(app)
    
    uvicorn.run(app, host=env.HOST_IP, port=env.HOST_PORT, debug=True)
