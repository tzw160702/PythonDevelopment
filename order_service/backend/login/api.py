# from typing import Any
# from fastapi import Request,APIRouter,Depends,Header,HTTPException
# import schemas
# import service
# from database import SessionLocal
# from sqlalchemy.orm import Session
#
# def get_db():
#
# admin_router = APIRouter()
#
# @admin_router.post('/auth/login',response_model=None,summary="使用账号密码登录")
# def login_access_token(
#         data: schemas.LogInByPwd,
#         request: Request,
#         db: Session = Depends(get_db)
# ):
#
#     return service.load_user(db,data)
# @admin_router.post('/auth/verify_code_login',response_model=None,summary="使用验证码登录")
# def verify_code_login(
#         data: schemas.LogInBycode,
#         request: Request,
#         db: Session = Depends(get_db)
# ):
#
#     return service.verify_code_login(db,data)
#
# @admin_router.post('/auth/register',summary="使用账号+密码+验证码注册")
# async def register(data: schemas.SignUp,
#         request: Request,
#         db: Session = Depends(get_db)):
#
#     return service.create_user(db,data)
#
# @admin_router.post('/send_code',summary="发送验证码")
# async def send_code(*,
#         request: Request,
#         number: str):
#   return service.send_code(number)
#
# @admin_router.post('/client_code',summary="客户端验证码生成")
# async def client_code(*,
#         request: Request):
#   return service.client_code()
#
# @admin_router.patch('/password',summary="修改密码")
# async def change_pwd(*,
#         data: schemas.ChangePwd,
#         request: Request,
#         db: Session = Depends(get_db)):
#   return service.change_pwd(db,data)
#
# @admin_router.patch('/verify_code_password',summary="忘记密码")
# async def verify_code_password(*,
#         data: schemas.SignUp,
#         request: Request,
#         db: Session = Depends(get_db)):
#   return service.verify_code_password(db,data)
#
