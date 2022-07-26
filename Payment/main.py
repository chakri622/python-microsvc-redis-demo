import requests, time
from starlette.requests import Request

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)
redis= get_redis_connection()


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  #pending, completed, refunded

    class Meta:
        database = redis


@app.get("/orders/{pk}")
def get(pk:str):
    order = Order.get(pk)
    #redis.xadd('refund_order', order.dict(), '*')
    return order


@app.post("/orders")
async def create(request: Request, background_tasks:BackgroundTasks): #id, quantity
    body = await request.json()
    print(body['id'])

    req = requests.get("http://localhost:8000/products/%s" % body['id'])
    product= req.json()
    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=product ['price'] * 0.20,
        total=1.2* product['price'],
        quantity=body['quantity'],
        status="pending"
    )
    order.save()
    background_tasks.add_task(order_completed,order)
    #order_completed(order)
    return order


def order_completed(order: Order):
    time.sleep(15)
    order.status='completed'
    order.save()
    print("Sending stream event")
    redis.xadd('order_completed', order.dict(), '*')
    print("Order sent")



