Pharmacy Management System

This is a mini project built using Python (Tkinter + CustomTkinter) and MySQL for managing pharmacy operations such as medicine inventory, billing, and orders.

Tech Stack:

- Python (Tkinter + CustomTkinter)
- MySQL
- Pillow (Image)
- mysql-connector-python

Features:

- Login & Register (Admin and Customer)
- Admin Dashboard: Add/View Medicines, Track Orders
- Customer Dashboard: View Medicines, Cart, Place Order
- Order Summary and Bill Generation

Screenshots:

> More in the `assets/` folder

🗃️ Database Tables

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

3. Set up MySQL database manually using the schema mentioned in `Documentation.docx`

## 📃 License

This project is for educational use.

