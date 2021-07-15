# #!/usr/bin/env python
# # -*- coding:utf-8 -*-
#
# from fastapi.exceptions import HTTPException
# import crud
# import json
# from sqlalchemy.orm import Session
# from util.utli import *
# from loguru import logger
# import common
# import env
# import requests
#
#
#
# # Admin
# def send_code(number):
#     urlbase = env.SINGLE_SIGN_ON_CODE+"/verify_code"
#     headers = {'Content-Type': 'application/json'}
#     url = urlbase+f"?number={number}"
#     # send data
#     response = requests.post(url=url,headers=headers)
#
#     return json.loads(response.text)
#
# def client_code():
#     url = env.SINGLE_SIGN_ON_CODE+"/client_code"
#     headers = {'Content-Type': 'application/json'}
#     response = requests.get(url=url,headers=headers)
#     return json.loads(response.text)
#
# def load_user(db:Session,data):
#     url = env.SINGLE_SIGN_ON_USER+"/singin"
#     headers = {'Content-Type': 'application/json'}
#     dataload = {"number":data.number,"pwd":data.pwd,"client_code":data.client_code,"callback_url":data.callback_url}
#     datas = json.dumps(dataload)
#     # send data
#     response = requests.post(url=url,data=datas,headers=headers)
#
#     return json.loads(response.text)
#
# def create_user(db:Session,data):
#
#     url = env.SINGLE_SIGN_ON_USER+"/signup"
#     headers = {'Content-Type': 'application/json'}
#     dataload = {"number":data.number,"pwd":data.pwd,"verify_code":data.verify_code}
#     datas = json.dumps(dataload)
#     # send data
#     response = requests.post(url=url,data=datas,headers=headers)
#
#     return json.loads(response.text)
#
# def change_pwd(db,data):
#     url = env.SINGLE_SIGN_ON_USER+"/password"
#     headers = {'Content-Type': 'application/json'}
#     dataload = {"token":data.token,"old_pwd":data.old_pwd,"new_pwd":data.new_pwd}
#     datas = json.dumps(dataload)
#     # send data
#     response = requests.patch(url=url,data=datas,headers=headers)
#
#     return json.loads(response.text)
# def verify_code_password(db,data):
#     url = env.SINGLE_SIGN_ON_USER+"/verify_code_password"
#     headers = {'Content-Type': 'application/json'}
#     dataload = {"number":data.number,"pwd":data.pwd,"verify_code":data.verify_code}
#     datas = json.dumps(dataload)
#     # send data
#     response = requests.patch(url=url,data=datas,headers=headers)
#
#     return json.loads(response.text)
