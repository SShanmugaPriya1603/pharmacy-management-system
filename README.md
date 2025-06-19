## Pharmacy Management System

This is a mini project built using Python (Tkinter + CustomTkinter) and MySQL for managing pharmacy operations such as medicine inventory, billing, and orders.

 ## Tech Stack:

- Python (Tkinter + CustomTkinter)
- MySQL
- Pillow (Image)
- mysql-connector-python

## Features:

- Login & Register (Admin and Customer)
- Admin Dashboard: Add/View Medicines, Track Orders
- Customer Dashboard: View Medicines, Cart, Place Order
- Order Summary and Bill Generation

## Screenshots:

> More in the `assets/` folder

## 🗃️ Database Tables

- `users(user_id, username, password, role)`
- `medicines(med_id, med_name, med_type, price, quantity)`
- `orders(order_id, user_id, order_date, total_amount)`
- `order_details(order_detail_id, order_id, med_id, quantity)`

## 🚀 Run Locally

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Start the app:
    ```bash
    python pharmacy_system/main.py
    ```

3. Set up MySQL database manually using the schema shown in the MySQL Database Setup section below.

      CREATE DATABASE pharmacy_db;
      USE pharmacy_db;
      
   CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    role ENUM('admin', 'customer') NOT NULL
);

CREATE TABLE medicines (
    med_id INT AUTO_INCREMENT PRIMARY KEY,
    med_name VARCHAR(100) NOT NULL,
    med_type VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_date DATETIME,
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE order_details (
    order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    med_id INT,
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (med_id) REFERENCES medicines(med_id)
);

## 📃 License

This project is for educational use.

