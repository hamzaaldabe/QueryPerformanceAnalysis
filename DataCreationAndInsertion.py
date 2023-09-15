import psycopg2
from faker import Faker
import random
from datetime import datetime

fake = Faker()
fake.MAX_UNIQUE_RETRY = 100000000 
db_params = {
    "host": "localhost",
    "database": "marketplace",
    "user": "hamza",
    "password": "14045111",
}

connection = psycopg2.connect(**db_params)
cursor = connection.cursor()

num_categories = 1000
num_products = 10 * 1024 * 1024 * 1024 // 775
num_users = 10 * 1024 * 1024 * 1024 // 92
num_orders = 10 * 1024 * 1024 * 1024 // 33
num_reviews = 10 * 1024 * 1024 * 1024 // 304

category_ids = []

for _ in range(num_categories):
    category_name = fake.word()
    cursor.execute(
        "INSERT INTO categories (category_name, parent_category_id) VALUES (%s, NULL)",
        (category_name,),
    )
  
    cursor.execute("SELECT LASTVAL()")
    category_id = cursor.fetchone()[0]
    category_ids.append(category_id)
    connection.commit()
    print(f"Inserted category: ID={category_id}, Name={category_name}")

for i in range(num_products):
    product_name = fake.first_name()
    description = fake.sentence()
    price = round(random.uniform(10, 1000), 2)
    stock_quantity = random.randint(1, 100)
    category_id = random.choice(category_ids) 
    cursor.execute(
        "INSERT INTO products (name, description, price, stock_quantity, category_id) "
        "VALUES (%s, %s, %s, %s, %s)",
        (product_name, description, price, stock_quantity, category_id),
    )
    connection.commit()
    print(f"Inserted product: Name={product_name}, Price={price}, Category ID={category_id}")

for _ in range(num_users):
    username = fake.user_name()
    email = fake.email()
    password = fake.password()
    registration_date = fake.date_time_this_decade()
    
    cursor.execute(
        "INSERT INTO users (username, email, password, registration_date) "
        "VALUES (%s, %s, %s, %s)",
        (username, email, password, registration_date),
    )
    connection.commit()
    print(f"Inserted user: Username={username}, Email={email}")

for _ in range(num_orders):
    user_id = random.randint(1, num_users)
    order_date = fake.date_time_between(start_date='-2y', end_date='now')
    status = random.choice(["Pending", "Shipped", "Delivered", "Cancelled"])
    total_amount = round(random.uniform(10, 1000), 2)

    cursor.execute(
        "INSERT INTO orders (user_id, order_date, status, total_amount) "
        "VALUES (%s, %s, %s, %s) RETURNING order_id",
        (user_id, order_date, status, total_amount),
    )
    
    order_id = cursor.fetchone()[0]
    connection.commit()
    print(f"Inserted order: Order ID={order_id}, User ID={user_id}, Status={status}")

    num_order_items = random.randint(1, 5) 
    for _ in range(num_order_items):
        product_id = random.randint(1, num_products)
        quantity = random.randint(1, 10)
        item_price = round(random.uniform(10, 100), 2)

        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, item_price) "
            "VALUES (%s, %s, %s, %s)",
            (order_id, product_id, quantity, item_price),
        )
        connection.commit()
        print(f"Inserted order item: Order ID={order_id}, Product ID={product_id}, Quantity={quantity}")

for _ in range(num_reviews):
    user_id = random.randint(1, num_users)
    product_id = random.randint(1, num_products)
    rating = random.randint(1, 5)
    review_text = fake.paragraph()
    review_date = fake.date_time_this_decade()

    cursor.execute(
        "INSERT INTO reviews (user_id, product_id, rating, review_text, review_date) "
        "VALUES (%s, %s, %s, %s, %s)",
        (user_id, product_id, rating, review_text, review_date),
    )
    connection.commit()
    print(f"Inserted review: User ID={user_id}, Product ID={product_id}, Rating={rating}")

connection.commit()
cursor.close()
connection.close()
