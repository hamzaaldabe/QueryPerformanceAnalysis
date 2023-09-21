import redis
import psycopg2
import simplejson as json
import datetime
from decimal import Decimal
redis_client = redis.Redis(host='localhost', port=6379, db=0)
db_connection = psycopg2.connect(
    host='localhost',
    database='marketplace',
    user='hamza',
    password='14045111'
)
cursor = db_connection.cursor()


class User:
    def __init__(self, user_id, username, email, password, registration_date):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.registration_date = registration_date

    def to_json(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "registration_date": self.registration_date.isoformat()
        }

class Product:
    def __init__(self,product_id,name,description,price,stock_quantity,category_id):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = Decimal(price)
        self.stock_quantity = stock_quantity
        self.category_id = category_id  
    def to_json(self):
        return{
            "product_id" : self.product_id,
            "name":self.name,
            "description":self.description,
            "price":self.price,
            "stock_quantity":self.stock_quantity,
            "category_id":self.category_id
        }
# cursor.execute("SELECT * FROM users")
# users = cursor.fetchall()

# for user_data in users:
#     user = User(*user_data)
#     user_key = f'user:{user.user_id}'
#     user_json = json.dumps(user.to_json())
#     redis_client.set(user_key, user_json)
#     print("Cached User wih ID: ", user_key)

cursor.execute("SELECT * FROM products")
products = cursor.fetchall()
for product_data in products:
    product = Product(*product_data)
    product_key = f'products:{product.product_id}'
    product_json = json.dumps(product.to_json())
    redis_client.set(product_key,product_json)
    print("Cached Product with ID ",product_key)
cursor.close()
db_connection.close()
