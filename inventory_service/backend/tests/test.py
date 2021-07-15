#!/usr/bin/python3

# 返回新增的主键
# main_id = [91, 92]
#
# # 外键
# for_id = [1, 2]

# for i in main_id:
#     k = 0
#     for v in for_id:
#
#         print(i, v)

# for k, v in enumerate(main_id):
#     print(k)

# 0
# 1

# from oslo_utils import uuidutils
#
# ls = uuidutils.generate_uuid(dashed=False)
# print(f'ls:{ls}')

# li = list()
# res = {'commodity_name': '商品名称', 'quantity_in_stock': 3000,
#        'spec': [{'spec_id': 5, 'spec_info_val': '规格值(数据类型不固定)'},
#                 {'spec_id': 3, 'spec_info_val': '规格值(数据类型不固定)'}],
#        'remark': '备注'}
#
# print(res["commodity_name"])


# get_spec = [{"spec_info_id": 27, "spec_id": 2, "spec_info_val": "擦嘴"}, {
#       "spec_info_id": 28, "spec_id": 3, "spec_info_val": "擦手"}]
#
# for i in get_spec:
#     print(i["spec_id"])

# li = [(59, 60)]
# ls = [{'spec_id': 3, 'spec_info_val':'喝茶'}, {'spec_id':4, 'spec_info_val':'容器'}]
# for index, val in enumerate(ls):
#     print(index, val)
#
# import os
#
# path = "F:/PythonDevelpment/backend/sql_app/tmpenj2vscn.jpg"
# os.remove(path)

# for infile in glob.glob(os.path.join(path, 'tmp70n0srot.jpg')):
#     os.remove(infile)
