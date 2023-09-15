CREATE TABLE users (
    user_id serial PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    registration_date TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE roles (
    role_id serial PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);


CREATE TABLE user_roles (
    user_id INT REFERENCES users(user_id),
    role_id INT REFERENCES roles(role_id),
    PRIMARY KEY (user_id, role_id)
);


CREATE TABLE categories (
    category_id serial PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    parent_category_id INT REFERENCES categories(category_id)
);


CREATE TABLE products (
    product_id serial PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL,
    category_id INT REFERENCES categories(category_id)
);


CREATE TABLE orders (
    order_id serial PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    order_date TIMESTAMP NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL
);


CREATE TABLE order_items (
    order_item_id serial PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL,
    item_price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE reviews (
    review_id serial PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    product_id INT REFERENCES products(product_id),
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    review_date TIMESTAMP NOT NULL DEFAULT NOW()
);
