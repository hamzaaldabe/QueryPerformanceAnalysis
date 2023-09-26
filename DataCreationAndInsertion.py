import psycopg2
from faker import Faker
import random
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

fake = Faker()
fake.MAX_UNIQUE_RETRY = 100000000

# Define your database connection parameters here
db_params = {
    "host": "localhost",
    "database": "marketplace",
    "user": "username",
    "password": "password",
}

# Function for inserting data into the categories table
def insert_categories(num_categories):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    category_ids = []

    for _ in tqdm(range(num_categories), desc="Inserting Categories"):
        category_name = fake.word()
        cursor.execute(
            "INSERT INTO categories (category_name, parent_category_id) VALUES (%s, NULL)",
            (category_name,),
        )

        cursor.execute("SELECT LASTVAL()")
        category_id = cursor.fetchone()[0]
        category_ids.append(category_id)

    connection.commit()
    cursor.close()
    connection.close()
    return category_ids

# Function for inserting data into the products table
def insert_products(num_products, category_ids):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    for _ in tqdm(range(num_products), desc="Inserting Products"):
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
    cursor.close()
    connection.close()

# Function for inserting data into the users table
def insert_users(num_users):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    for _ in tqdm(range(num_users), desc="Inserting Users"):
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
    cursor.close()
    connection.close()

# Function for inserting data into the orders table
def insert_orders(num_orders, num_users, num_products):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    for _ in tqdm(range(num_orders), desc="Inserting Orders"):
        user_id = random.randint(1, num_users)
        order_date = fake.date_time_between(start_date='-2y', end_date='now')
        status = random.choice(["Pending", "Shipped", "Delivered", "Cancelled"])
        total_amount = round(random.uniform(10, 1000), 2)

        cursor.execute(
            "INSERT INTO orders (user_id, order_date, status, total_amount) "
            "VALUES (%s, %s, %s, %s) RETURNING order_id",
            (user_id, order_date, status, total_amount),
        )

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
    cursor.close()
    connection.close()

# Function for inserting data into the reviews table
def insert_reviews(num_reviews, num_users, num_products):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    for _ in tqdm(range(num_reviews), desc="Inserting Reviews"):
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
    cursor.close()
    connection.close()

if __name__ == "__main__":
    num_categories = 1000
    num_products = 3000000
    num_users = 3000000
    num_orders = 3000000
    num_reviews = 3000000

    # Create a thread pool executor to run functions concurrently
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit tasks to the executor
        categories_future = executor.submit(insert_categories, num_categories)
        products_future = executor.submit(insert_products, num_products, categories_future.result())
        users_future = executor.submit(insert_users, num_users)
        orders_future = executor.submit(insert_orders, num_orders, num_users, num_products)
        reviews_future = executor.submit(insert_reviews, num_reviews, num_users, num_products)

    print("All tasks have been submitted.")
