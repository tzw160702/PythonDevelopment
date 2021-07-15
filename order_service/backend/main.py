#!/usr/bin/python3

import uvicorn
from core.api import app, order_router, login_router, shop_car_router


app.include_router(order_router)
app.include_router(login_router)
app.include_router(shop_car_router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, debug=True)


