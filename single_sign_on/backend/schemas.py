from pydantic import BaseModel
from pydantic.fields import Field
from typing import List, Optional


class StatusCode(BaseModel):
    status: int = Field(title='状态码', description='状态码')
    message: str = Field(title='状态信息说明', description='状态信息说明')


class Page(BaseModel):
    data_count: int = Field(0, title="数据总长度", description="数据总长度")
    page_count: int = Field(0, title="总页数", description="总页数")
    page: int = Field(0, title="当前页数", description="当前页数")
    page_size: int = Field(0, title="每页数据长度", description="每页数据长度")


class LogInByPwd(BaseModel):
    number: str = Field(title='手机号或者邮箱', description='手机号或者邮箱')
    pwd: str = Field(title='密码', description='密码')
    client_code: str = Field(title='客户端验证码', description='客户端验证码')
    callback_url: str = Field(title='系统回调地址', description='系统回调地址')


class LogInBycode(BaseModel):
    number: str = Field(title='手机号或者邮箱', description='手机号或者邮箱')
    verify_code: str = Field(title='手机或邮箱验证码', description='手机或邮箱验证码')
    callback_url: str = Field(title='系统回调地址', description='系统回调地址')


class ResponseLog(BaseModel):
    status: int = Field(title='状态码', description='状态码')
    token: Optional[str] = Field(title='token', description='token')
    message: Optional[str] = Field(title='信息说明', description='信息说明')


class ResponseSignIn(BaseModel):
    token: str = Field(title='token', description='token')
    express_time: int = Field(title='token有效时间', description='token有效时间')


class UserInfo(BaseModel):
    username: Optional[str] = Field(title='用户名称', description='用户名称')
    phone: Optional[str] = Field(title='手机号码', description='手机号码')
    email: Optional[str] = Field(title='邮箱', description='邮箱')


class UserInfos(UserInfo):
    status: int = Field(title='用户状态', description='用户状态')

    class Config:
        orm_mode = True


class SignUp(BaseModel):
    number: str = Field(title='手机号或者邮箱', description='手机号或者邮箱')
    pwd: str = Field(title='密码', description='密码')
    verify_code: str = Field(title='验证码', description='验证码')


class VerifyToken(BaseModel):
    token: str = Field(title='Token', description='Token')
    sys_ip: str = Field(title='系统地址', description='系统地址')


class VerifyUserInfo(BaseModel):
    token: str = Field(title='Token', description='Token')
    callback_url: str = Field(title='系统回调地址', description='系统回调地址')


class ChangePwd(BaseModel):
    token: str = Field(title='Token', description='Token')
    old_pwd: str = Field(title='旧密码', description='旧密码')
    new_pwd: str = Field(title='新密码', description='新密码')


class CodeInfo(BaseModel):
    client_code: str = Field(title='客户端验证码', description='客户端验证码')
    express_time: int = Field(title='验证码有效时间', description='验证码有效时间')


class ResponseUser(BaseModel):
    data: UserInfo = Field(title='用户信息', description='用户信息')
    message: str = Field(title='信息说明', description='信息说明')

    class Config:
        orm_mode = True


class ResponseUsers(Page):
    data: List[UserInfos] = Field([], title='用户信息', description='用户信息')
    # message: str = Field(title='信息说明', description='信息说明')

    class Config:
        orm_mode = True

class Users(BaseModel):
    message: str = Field(title='信息说明', description='信息说明')
    data: ResponseUsers = Field( title='用户信息', description='用户信息')
    # code: str = Field(title='状态码', description='状态码')

    class Config:
        orm_mode = True