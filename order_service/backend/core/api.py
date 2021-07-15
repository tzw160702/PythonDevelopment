#!/usr/bin/python3

from typing import List
from core import schemas
from sql_app import crud
from typing import Optional
from sqlalchemy.orm import Session
from sql_app.database import session
from fastapi import (File,
                     Depends,
                     FastAPI,
                     APIRouter,
                     UploadFile)
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# 用作静态文档访问
app.mount("/backend", StaticFiles(directory="resources"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------- 数据库操作依赖 ---------------------------
def get_database():
    db = ''
    try:
        db = session
        yield db
    finally:
        db.close()


# ---------------------------- 订单 -----------------------------------
# 注册订单路由
order_router = APIRouter(tags=["Order"], prefix="/order")

# 全部订单
@order_router.get("/", response_model=schemas.Data)
async def all_order(page: int,
                    limit: Optional[int] = 5,
                    db: Session = Depends(get_database)):
    return crud.fetch_all_order(page=page, limit=limit, db=db)


# 已完成
@order_router.get("/order_done", response_model=schemas.Data)
async def done_order(page: int,
                     limit: Optional[int] = 5,
                     db: Session = Depends(get_database)):
    return crud.fetch_done_order(page=page, limit=limit, db=db)


# 未支付
@order_router.get("/oder_undone", response_model=schemas.Data)
async def undone_order(page: int,
                       limit: Optional[int] = 5,
                       db: Session = Depends(get_database)):
    return crud.fetch_undone_order(page=page, limit=limit, db=db)


# 订单详情
@order_router.get("/{order_id}", response_model=schemas.DetailsOrder)
async def fetch_order_details(order_id: int,
                              db: Session = Depends(get_database)):
    return crud.order_details(order_id=order_id, db=db)


# 修改订单
@order_router.patch("/{order_id}", response_model=schemas.DetailsOrder)
async def modify_order(update_order: schemas.UpdateOrder,
                       db: Session = Depends(get_database)):
    return crud.db_update_order(update_order=update_order, db=db)


# 删除订单
@order_router.delete("/{order_id}")
async def del_order(order_id: int, db: Session = Depends(get_database)):
    return crud.db_del_order(order_id=order_id, db=db)

# --------------------------- 购物车 ----------------------------------
# 注册购物车路由
shop_car_router = APIRouter(tags=["ShopCar"], prefix="/cart")


# 购物车列表
@shop_car_router.get('/', response_model=List[schemas.ShopCar])
async def cart_commodity(db: Session = Depends(get_database)):
    return crud.all_comm(db=db)


@shop_car_router.delete('/{commodity_id}')
async def del_commodity(commodity_id: int, db: Session = Depends(get_database)):
    return crud.del_comm(commodity_id=commodity_id, db=db)

# ---------------------------- 登录 ----------------------------------
# 注册登录路由
login_router = APIRouter(tags=["Login"])


@login_router.post('/auth/login', summary="使用账号密码登录")
def login_access_token(data: schemas.LogInByPwd):
    return crud.load_user(data=data)


@login_router.post('/send_code', summary="发送验证码")
async def send_code(*, number: str):
    return crud.send_code(number)


@login_router.post('/auth/verify_code_login', summary="使用验证码登录")
def verify_code_login(data: schemas.LogInByCode):
    return crud.verify_code_login(data=data)


@login_router.post('/auth/register', summary="使用账号+密码+验证码注册")
async def register(data: schemas.SignUp):
    return crud.create_user(data=data)


@login_router.post('/client_code', summary="客户端验证码生成")
async def client_code():
    return crud.client_code()


@login_router.patch('/password', summary="修改密码")
async def change_pwd(*, data: schemas.ChangePwd):
    return crud.change_pwd(data=data)


@login_router.patch('/verify_code_password', summary="忘记密码")
async def verify_code_password(*, data: schemas.SignUp):
    return crud.verify_code_password(data=data)


# 上传文件
@app.post("/file")
async def upload_file(files: List[UploadFile] = File(...)):
    return crud.upload(files=files)
