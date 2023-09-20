import redis
import psycopg2
import json
import datetime

redis_client = redis.Redis(host='localhost', port=6379, db=0)
db_connection = psycopg2.connect(
    host='localhost',
    database='marketplace',
    user='hamza',
    password='password'
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


cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

for user_data in users:
    user = User(*user_data)
    user_key = f'user:{user.user_id}'
    user_json = json.dumps(user.to_json())
    redis_client.set(user_key, user_json)
    print("Cached User wih ID: ", user_key)
cursor.close()
db_connection.close()
