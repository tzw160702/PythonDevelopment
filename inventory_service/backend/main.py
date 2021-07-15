#!/usr/bin/python3

import uvicorn
from core.api import (app,
                      type_router,
                      spec_router,
                      data_type_router,
                      commodity_router)

# 添加路由
app.include_router(type_router)
app.include_router(data_type_router)
app.include_router(spec_router)
app.include_router(commodity_router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, debug=True)


