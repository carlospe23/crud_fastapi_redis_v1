from fastapi import APIRouter
from schemas.product import Product
from redis_client.crud import save_hash, get_hash, delete_hash


routes_product = APIRouter()

fake_db = [
    {
        "id": "8b665697-9803-4a22-90c8-68adfc4507d0",
        "name": "string",
        "price": 12.9,
        "date": "2023-03-06 01:54:54.098274"
    }
]


@routes_product.post('/create', response_model=Product)
def create(product: Product):
    try:
        # OPERATION DB

        fake_db.append(product.dict())

        #OPREATIONS CACHE
        save_hash(key=product.dict()['id'], data=product.dict())

        return product

    except Exception as e:
        return e


@routes_product.get('/product/{id}')
def get(id: str):
    try:
        #OPERACION CACHE
        data = get_hash(key=id)
        if len(data) == 0:
            #OPERATION DB
            product = list(filter(lambda field: field['id'] == id, fake_db))[0]
            #OPERATION CACHE
            save_hash(key=id, data=product)
            return product
        return data
    except Exception as e:
        return e


@routes_product.delete('/delete/{id}')
def get(id: str):
    try:
        _keys = Product.__fields__.keys()
        #OPERATION CACHE
        delete_hash(key=id, keys=_keys)
        # OPERATION DB
        product = list(filter(lambda field: field['id'] == id, fake_db))[0]
        if len(product) != 0:
            fake_db.remove(product)

        return {
            'Message': 'Succes',
            'products': fake_db
        }

    except Exception as e:
        return e

