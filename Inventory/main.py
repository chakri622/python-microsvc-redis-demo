from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)
redis= get_redis_connection()

    #get_redis_connection(host="redis-15343.c14.us-east-1-2.ec2.cloud.redislabs.com",
     #                       port=15343,
      #                      password="AVydu8whYebgofQ6PclTF9cKUxEsOoSH", decode_responses=True)

#get_redis_connection()

#redis.flushdb()

print(redis)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database: redis


@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]
    #return format("01G87EMVYBW0JNP3G3WF6WVNDJ")
     #return Product.all_pks()


def format(pk: str):
    print(pk)
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.post('/products')
def create(product: Product):
    print(product)
    return product.save()



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/products/{pk}")
def get(pk: str):
    return Product.get(pk)


@app.delete("/products/{pk}")
def delete(pk: str):
    return Product.delete(pk)