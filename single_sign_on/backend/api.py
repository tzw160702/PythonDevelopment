from fastapi import (Request, APIRouter, Depends)
import schemas
import service
import env

from sqlalchemy.orm import Session
from database import SessionLocal
import json

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


code_router = APIRouter()


# 发送短信或者邮箱的验证码
@code_router.post("/verify_code", tags=["code"], response_model=schemas.StatusCode, summary="发送短信或者邮箱的验证码")
async def verify_code(
        *,
        request: Request,
        number: str
):
    result, message = service.get_verify_code(number=number)
    if not result:
        return {"status": 4001, "message": message}
    # 将验证码存储到 redis 中
    await request.app.state.redis.set(f"{number}", result, expire=env.EFFECTIVE_TIME_SMS)
    return {"status": 200, "message": message}


#  获取客户端验证码
@code_router.get("/client_code",
                 tags=["code"],
                 summary="获取客户端验证码")
async def get_client_code(request: Request):
    client_code = service.get_client_code()
    await request.app.state.redis.set(f"{client_code}", client_code, expire=env.EFFECTIVE_TIME_CLIENT)
    return {"client_code": client_code}


login_router = APIRouter()


# # 用户使用密码登陆
@login_router.post("/singin",
                   tags=["users"],
                   response_model=schemas.ResponseLog,
                   summary="用户使用密码登陆")
async def sign_in(
        data: schemas.LogInByPwd,
        request: Request,
        db: Session = Depends(get_db)):
    redis_client_code = await request.app.state.redis.get(data.client_code)
    userid, token, message = service.sign_in(db, request, obj_in=data, redis_client_code=redis_client_code)
    if userid:
        await request.app.state.redis.set(f"{data.client_code}", "", expire=1)  # 是客户端验证码失效
        await request.app.state.redis.set(f"{userid}", token, expire=env.ACCESS_TOKEN_EXPIRE_SECONDS)    # 将token存储到redis中
        return {"status": 200, "token": token, "message": message}
    return {"status": 4001, "token": token, "message": message}
    

# 使用验证码登录
@login_router.post("/signin/verifycode",
                   tags=["users"],
                   response_model=schemas.ResponseLog,
                   summary="使用验证码登录")
async def sign_in_by_code(
        data: schemas.LogInBycode,
        request: Request,
        db: Session = Depends(get_db)):
    # 在redis中获取验证码
    redis_verify_code = await request.app.state.redis.get(data.number)
    userid, token, message = service.sign_in_by_code(db, request, obj_in=data, redis_verify_code=redis_verify_code)
    # 将token存储到redis中
    if userid:
        await request.app.state.redis.set(f"{data.number}", "", expire=1)
        await request.app.state.redis.set(f"{userid}", token, expire=env.ACCESS_TOKEN_EXPIRE_SECONDS)
        return {"status": 200, "token": token, "message": message}
    return {"status": 4001, "token": token, "message": message}


# 用户注册接口
@login_router.post("/signup",
                   tags=["users"],
                   response_model=schemas.StatusCode,
                   summary="用户注册接口")
async def user_signup(
        data: schemas.SignUp,
        request: Request,
        db: Session = Depends(get_db)):
    redis_verify_code = await request.app.state.redis.get(data.number)      # 获取 redis 中验证码
    userid, message = service.user_signup(db, obj_in=data, redis_verify_code=redis_verify_code)
    if not userid:
        return {"status": 4001, "message": message}
    await request.app.state.redis.set(f'{data.number}', '', expire=1)  # 使验证码失效
    return {"status": 200, "message": message}


# 修改密码
@login_router.patch("/password",
                    tags=["users"],
                    response_model=schemas.StatusCode,
                    summary="修改密码")
async def change_password(
        data: schemas.ChangePwd,
        request: Request,
        db: Session = Depends(get_db)):
    userid, message = service.change_password(db, obj_in=data)
    if userid:
        await request.app.state.redis.set(f"{userid}", '', expire=1)
        return {"status": 200, "message": message}
    return {"status": 4001, "message": message}


# 忘记密码
@login_router.patch("/verify_code_password",
                    tags=["users"],
                    response_model=schemas.StatusCode,
                    summary="忘记密码")
async def forgot_password(
        data: schemas.SignUp,
        request: Request,
        db: Session = Depends(get_db)):
    # 获取 redis 中验证码
    redis_verify_code = await request.app.state.redis.get(data.number)
    userid, message = service.forgot_password(db, obj_in=data, redis_verify_code=redis_verify_code)
    if not userid:
        return {"status": 4001, "message": message}
    await request.app.state.redis.set(f"{data.number}", "", expire=1)   # 使验证码失效
    await request.app.state.redis.set(f"{userid}", "", expire=1)        # 使 redis 中 token 失效
    return {"status": 200, "message": message}


# 根据用户id查询用户信息
@login_router.get("/{userid}",
                  tags=["users"],
                  response_model=schemas.ResponseUser,
                  summary="根据用户id查询用户信息")
async def get_userinfo_by_id(
        userid: int,
        db: Session = Depends(get_db)):
    data, message = service.get_userinfo_by_id(db, userid)
    return {"data":data.__dict__, "message":message}


# 查询所有用户信息
@login_router.get("/",
                  tags=["users"],
                  response_model=schemas.Users,
                  summary="查询所有用户信息")
async def get_users(
        db: Session = Depends(get_db), paginate='{"page":1,"limit":10}',
        filter='[{"fieldname":"id","option":"is_not_null"}]', sort='[{"field":"id","direction":"desc"}]'):
    data, message = service.get_users(db, paginate, filter, sort)
    datas = {"message":message,"data":data}
    
    return datas


# 查询token对应的用户信息接口
@login_router.get("/token/",
                  tags=["users"],
                  response_model=schemas.ResponseUser,
                  summary="查询token对应的用户信息接口")
async def get_userinfo_by_token(token: str, db: Session = Depends(get_db)):
    data, message = service.get_userinfo_by_token(db, token)
    return {"data": data.__dict__, "message": message}


# 用户修改信息
@login_router.put("/users",
                  tags=["users"],
                  response_model=schemas.ResponseUser,
                  summary="用户修改信息")
async def update_userinfo_by_token(
        data: schemas.UserInfo,
        token: str,
        db: Session = Depends(get_db)):
    data, message = service.update_userinfo_by_token(db, obj_in=data, token=token)
    return {"data": data.__dict__, "message": message}


# # 修改用户状态信息
# @login_router.patch("/{id}",
#                     tags=["users"],
#                     response_model=schemas.UserInfos,
#                     summary="修改用户状态信息")
# async def update_userinfo_by_id(data:schemas.UserInfo,
#                     db: Session = Depends(get_db)):
#     return service.update_userinfo_by_id(db,obj_in=data)


# 退出登录
@login_router.patch("/signout",
                    tags=["users"],
                    response_model=schemas.StatusCode,
                    summary="退出登录")
async def logout(
        token: str,
        request: Request,
        db: Session = Depends(get_db)):
    data, message = service.user_signout(db, token=token)
    if data:
        await request.app.state.redis.set(f'{data}', '', expire=1)
        return {"status": 200, "message": message}
    return {"status": 4001, "message": message}


# 注销用户
@login_router.delete("/users",
                     tags=["users"],
                     response_model=schemas.StatusCode,
                     summary="注销用户")
async def user_log_off(token: str,
                       request: Request,
                       db: Session = Depends(get_db)):
    userid, message = service.user_log_off(db, token=token)
    if not userid:
        return {"status": "4001", "message": message}
    await request.app.state.redis.set(f'{userid}', '', expire=1)
    return {"status": "200", "message": message}


token_router = APIRouter()


# 校验token
@token_router.get("/auth",
                  tags=["token"],
                  response_model=schemas.StatusCode,
                  summary="校验token")
async def verify_token(token: str, request: Request):
    data, message = await service.verify_token(request, token=token)
    if not data:
        return {"status": 4001, "message": message}
    return {"status": 200, "message": message}


# 校验token是否有效并添加用户在其他系统的登陆信息
@token_router.post("/token",
                  tags=["token"],
                  response_model=schemas.StatusCode,
                  summary="校验token是否有效并添加用户在其他系统的登陆信息")
async def verify_token(
        obj_in: schemas.VerifyUserInfo,
        request: Request,
        db: Session = Depends(get_db)
):
    data, message = await service.verify_token_add_info(db, request, obj_in=obj_in)
    if not data:
        return {"status": 4001, "message": message}
    return {"status": 200, "message": message}
