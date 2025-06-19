import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from PIL import Image,ImageTk
from datetime import datetime

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="admin123",
            password="priya",
            database="pharmacy_db"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to database: {err}")
        return None

def login():
    username = entry_username.get()
    password = entry_password.get()

    # Connect to the database
    db = connect_db()
    if not db:
        return
    cursor = db.cursor()


    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()
    if result:
        user_id, username, password, role = result
        messagebox.showinfo("Login", "Login Successful!")
        if role == "admin":
            open_admin_dashboard(user_id)
        else:
            open_customer_dashboard(user_id)
    else:
        messagebox.showerror("Login", "Invalid username or password!")

    cursor.close()
    db.close()

def open_admin_dashboard(user_id):
    root.withdraw()
    admin_window = ctk.CTkToplevel()
    admin_window.geometry("800x600")
    admin_window.title("Admin Dashboard")


    ctk.CTkLabel(admin_window, text="Admin Dashboard", font=("Arial", 18)).pack(pady=10)
    ctk.CTkButton(admin_window, text="View Medicines", command=lambda: view_medicines(admin_window)).pack(pady=15)
    ctk.CTkButton(admin_window, text="Add Medicine", command=lambda: add_medicine(admin_window)).pack(pady=15)
    ctk.CTkButton(admin_window, text="Track Orders", command=lambda: track_orders(admin_window)).pack(pady=15)
    ctk.CTkButton(admin_window, text="Logout", command=lambda: logout(admin_window)).pack(pady=15)

    admin_window.protocol("WM_DELETE_WINDOW", lambda: logout(admin_window))

def open_customer_dashboard(user_id):
    root.withdraw()  # Close the login window
    customer_window = ctk.CTkToplevel()
    customer_window.geometry("800x600")
    customer_window.title("Customer Dashboard")


    ctk.CTkLabel(customer_window, text="Customer Dashboard", font=("Arial", 18)).pack(pady=10)
    ctk.CTkButton(customer_window, text="View Medicines", command=lambda: view_medicines(customer_window)).pack(pady=15)
    ctk.CTkButton(customer_window, text="View Cart", command=lambda: view_cart(user_id, customer_window)).pack(pady=15)
    ctk.CTkButton(customer_window, text="Place Order", command=lambda: place_order(user_id, customer_window)).pack(
        pady=15)
    ctk.CTkButton(customer_window, text="Logout", command=lambda: logout(customer_window)).pack(pady=15)

    customer_window.protocol("WM_DELETE_WINDOW", lambda:logout(customer_window))

def view_medicines(window):
    view_window = ctk.CTkToplevel(window)
    view_window.title("View Medicines")


    canvas = ctk.CTkCanvas(view_window)
    scrollbar = ctk.CTkScrollbar(view_window, orientation="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)


    frame = ctk.CTkFrame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")


    frame.grid_rowconfigure(0, weight=2)  # Allow rows to expand
    frame.grid_columnconfigure(0, weight=2)  # Allow the first column to expand

    db = connect_db()
    if db:
        cursor = db.cursor()
        query = "SELECT med_id, med_name, quantity, price FROM medicines"
        cursor.execute(query)
        medicines = cursor.fetchall()

        # Loop through the medicines and create labels with formatted data
        for index, medicine in enumerate(medicines):
            med_id, med_name, quantity, price = medicine
            label = ctk.CTkLabel(frame, text=f"ID: {med_id} | Name: {med_name} | Quantity: {quantity} | Price: ₹{price:.2f}", width=2500, anchor="w")
            label.grid(row=index, column=0, padx=10, pady=5, sticky="w")

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))


        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        db.close()


def add_medicine(window):
    # Create a new window for adding medicines
    add_window = ctk.CTkToplevel(window)
    add_window.title("Add Medicine")

    # Create labels and entry fields for the new medicine details
    ctk.CTkLabel(add_window, text="Medicine Name:").grid(row=0, column=0, padx=10, pady=10)
    med_name_entry = ctk.CTkEntry(add_window)
    med_name_entry.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkLabel(add_window, text="Medicine Type:").grid(row=1, column=0, padx=10, pady=10)
    med_type_entry = ctk.CTkEntry(add_window)
    med_type_entry.grid(row=1, column=1, padx=10, pady=10)

    ctk.CTkLabel(add_window, text="Price:").grid(row=2, column=0, padx=10, pady=10)
    price_entry = ctk.CTkEntry(add_window)
    price_entry.grid(row=2, column=1, padx=10, pady=10)

    ctk.CTkLabel(add_window, text="Quantity:").grid(row=3, column=0, padx=10, pady=10)
    quantity_entry = ctk.CTkEntry(add_window)
    quantity_entry.grid(row=3, column=1, padx=10, pady=10)

    # Function to submit the new medicine details
    def submit_addition():
        # Get the details from the entry fields
        med_name = med_name_entry.get()
        med_type = med_type_entry.get()
        price = price_entry.get()
        quantity = quantity_entry.get()

        # Validate the input data
        if not med_name or not med_type or not price or not quantity:
            messagebox.showerror("Input Error", "All fields must be filled in.")
            return

        if not price.replace('.', '', 1).isdigit() or not quantity.isdigit():
            messagebox.showerror("Input Error", "Please enter valid numeric values for price and quantity.")
            return

        # Establish a connection to the database
        try:
            db = connect_db()
            if db:
                cursor = db.cursor()

                # Insert the new medicine into the database
                query = "INSERT INTO medicines (med_name, med_type, price, quantity) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (med_name, med_type, float(price), int(quantity)))

                db.commit()  # Commit the changes to the database

                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", f"Medicine '{med_name}' added successfully.")
                else:
                    messagebox.showerror("Error", "Failed to add the medicine.")
                db.close()  # Close the connection

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error adding medicine: {err}")

        add_window.destroy()  # Close the add window after submission

    # Submit button
    submit_button = ctk.CTkButton(add_window, text="Add Medicine", command=submit_addition)
    submit_button.grid(row=4, column=0, columnspan=2, pady=10)

# Track Orders (Admin functionality)
def track_orders(window):
    track_window = ctk.CTkToplevel(window)
    track_window.title("Track Orders")

    try:
        # Ensure database connection is established
        db = connect_db()
        if db:
            cursor = db.cursor()

            # Query to fetch all orders
            query = """
                    SELECT o.order_id, u.user_id, o.order_date, o.total_amount
                    FROM orders o
                    JOIN users u ON o.user_id = u.user_id
                    ORDER BY o.order_date DESC
                """
            cursor.execute(query)
            orders = cursor.fetchall()

            if not orders:
                messagebox.showinfo("No Orders", "No orders found.")
                return

            # Create a frame to hold the order details in a scrollable area
            order_frame = ctk.CTkScrollableFrame(track_window)
            order_frame.grid(row=0, column=0, padx=10, pady=10)

            # Header row
            ctk.CTkLabel(order_frame, text="Order ID", width=100, anchor="w").grid(row=0, column=0, padx=10, pady=5)
            ctk.CTkLabel(order_frame, text="User ID", width=100, anchor="w").grid(row=0, column=1, padx=10, pady=5)
            ctk.CTkLabel(order_frame, text="Order Date", width=150, anchor="w").grid(row=0, column=2, padx=10, pady=5)
            ctk.CTkLabel(order_frame, text="Total Amount", width=100, anchor="w").grid(row=0, column=3, padx=10, pady=5)

            # Display the orders
            for index, order in enumerate(orders, start=1):
                order_id, user_id, order_date, total_amount = order
                ctk.CTkLabel(order_frame, text=str(order_id), width=100, anchor="w").grid(row=index, column=0, padx=10,
                                                                                          pady=5)
                ctk.CTkLabel(order_frame, text=str(user_id), width=100, anchor="w").grid(row=index, column=1, padx=10,
                                                                                         pady=5)
                ctk.CTkLabel(order_frame, text=str(order_date), width=150, anchor="w").grid(row=index, column=2,
                                                                                            padx=10, pady=5)
                ctk.CTkLabel(order_frame, text=f"${total_amount:.2f}", width=100, anchor="w").grid(row=index, column=3,
                                                                                                   padx=10, pady=5)

            db.close()  # Ensure the connection is closed after use
        else:
            messagebox.showerror("Connection Error", "Failed to connect to the database.")

    except Exception as e:
        messagebox.showerror("Error", f"Error fetching orders: {str(e)}")
    pass





# View Cart (Customer functionality)
def view_cart(user_id,window):


    # Connect to the database
    db = connect_db()
    if not db:
        return
    try:
        cursor = db.cursor()

        # Fetch the cart details
        query = """
            SELECT m.med_name, od.quantity 
            FROM orders o
            JOIN order_details od ON o.order_id = od.order_id
            JOIN medicines m ON od.med_id = m.med_id
            WHERE o.user_id = %s
        """
        cursor.execute(query, (user_id,))
        cart = cursor.fetchall()

        # Prepare the cart details for display
        if not cart:
            cart_summary = "Your cart is empty."
        else:
            cart_summary = "Your Cart:\n\n"
            cart_summary += f"{'Medicine':<20}{'Quantity':<10}\n"
            cart_summary += "-" * 30 + "\n"
            for item in cart:
                medicine_name, quantity = item
                cart_summary += f"{medicine_name:<20}{quantity:<10}\n"

        # Show the cart in a messagebox
        messagebox.showinfo("Cart", cart_summary)

    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch cart: {str(e)}")
    finally:
        # Close the cursor and database connection
        cursor.close()
        db.close()


# Place Order (Customer functionality)


def generate_bill(order_id, user_id, cursor):
    try:
        # Fetch order details
        cursor.execute("""
            SELECT od.med_id, m.med_name, od.quantity, od.price 
            FROM order_details od 
            JOIN medicines m ON od.med_id = m.med_id 
            WHERE od.order_id = %s
        """, (order_id,))
        items = cursor.fetchall()

        if not items:
            return "No items found for the given order ID."

        # Generate bill content
        bill = f"Order ID: {order_id}\nCustomer ID: {user_id}\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        bill += "Items:\n"
        bill += f"{'Medicine':<20}{'Quantity':<10}{'Price':<10}\n"
        bill += "-" * 40 + "\n"

        total = 0
        for item in items:
            med_name, quantity, price = item[1], item[2], item[3]
            bill += f"{med_name:<20}{quantity:<10}{price:<10.2f}\n"
            total += quantity * price

        bill += "-" * 40 + "\n"
        bill += f"{'Total':<30}{total:.2f}\n"
        return bill
    except Exception as e:
        return f"Error generating bill: {str(e)}"

def place_order(user_id, window):


    # Open Place Order window
    order_window = ctk.CTkToplevel(window)
    order_window.title("Place Order")

    db = connect_db()
    if not db:
        return

    try:
        cursor = db.cursor()

        # Fetch medicines from the database
        query = "SELECT med_id, med_name, price FROM medicines"
        cursor.execute(query)
        medicines = cursor.fetchall()

        # ComboBox for selecting medicines
        ctk.CTkLabel(order_window, text="Select Medicine:").grid(row=0, column=0, padx=10, pady=10)
        medicine_listbox = ctk.CTkComboBox(order_window,
                                           values=[f"{med[0]} - {med[1]} - ₹{med[2]}" for med in medicines])
        medicine_listbox.grid(row=0, column=1, padx=10, pady=10)

        # Entry for quantity
        ctk.CTkLabel(order_window, text="Quantity:").grid(row=1, column=0, padx=10, pady=10)
        quantity_entry = ctk.CTkEntry(order_window)
        quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        # Define submit_order function
        def submit_order():
            selected_medicine = medicine_listbox.get()
            quantity = quantity_entry.get()

            # Validate inputs
            if not selected_medicine:
                messagebox.showerror("Input Error", "Please select a medicine.")
                return
            if not quantity.isdigit() or int(quantity) <= 0:
                messagebox.showerror("Input Error", "Please enter a valid quantity.")
                return

            # Extract medicine ID and price
            med_id = int(selected_medicine.split(" - ")[0])
            price = float(selected_medicine.split(" - ₹")[1])
            quantity = int(quantity)

            # Reconnect to ensure cursor is valid
            db_reconnect = connect_db()
            if not db_reconnect:
                return

            try:
                cursor_reconnect = db_reconnect.cursor()

                # Check stock availability
                cursor_reconnect.execute("SELECT quantity FROM medicines WHERE med_id = %s", (med_id,))
                stock_quantity = cursor_reconnect.fetchone()

                if stock_quantity and quantity <= stock_quantity[0]:
                    # Calculate total price
                    total_price = quantity * price

                    # Insert into orders table
                    order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cursor_reconnect.execute(
                        "INSERT INTO orders (user_id, order_date, total_amount) VALUES (%s, %s, %s)",
                        (user_id, order_date, total_price))
                    db_reconnect.commit()

                    # Get the generated order ID
                    cursor_reconnect.execute("SELECT LAST_INSERT_ID()")
                    order_id = cursor_reconnect.fetchone()[0]

                    # Insert into order_details table
                    cursor_reconnect.execute(
                        "INSERT INTO order_details (order_id, med_id, quantity, price) VALUES (%s, %s, %s, %s)",
                        (order_id, med_id, quantity, price))
                    db_reconnect.commit()

                    # Update stock
                    cursor_reconnect.execute("UPDATE medicines SET quantity = quantity - %s WHERE med_id = %s",
                                             (quantity, med_id))
                    db_reconnect.commit()

                    # Generate and display bill
                    bill = generate_bill(order_id, user_id, cursor_reconnect)
                    messagebox.showinfo("Order Bill", bill)

                    # Optionally save the bill to a file
                    with open(f"Bill_{order_id}.txt", "w") as bill_file:
                        bill_file.write(bill)

                    # Close the order window
                    order_window.destroy()
                else:
                    messagebox.showerror("Error", "Insufficient stock or invalid quantity.")

            except Exception as e:
                messagebox.showerror("Database Error", f"Error interacting with the database: {str(e)}")
            finally:
                cursor_reconnect.close()
                db_reconnect.close()

        # Place Order Button
        ctk.CTkButton(order_window, text="Place Order", command=submit_order).grid(row=2, column=0, columnspan=2, pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"Error loading medicines: {str(e)}")
    finally:
        cursor.close()
        db.close()


def logout(window):
    window.destroy()
    root.deiconify()

def open_register_window():
    register_window = ctk.CTkToplevel(root)
    register_window.title("Register")
    register_window.geometry("300x350")

    # Username Entry
    label_username = ctk.CTkLabel(register_window, text="Username:")
    label_username.pack(pady=10)
    entry_username_reg = ctk.CTkEntry(register_window)
    entry_username_reg.pack(pady=5)

    # Password Entry
    label_password = ctk.CTkLabel(register_window, text="Password:")
    label_password.pack(pady=10)
    entry_password_reg = ctk.CTkEntry(register_window, show="*")
    entry_password_reg.pack(pady=5)

    # Role Selection
    label_role = ctk.CTkLabel(register_window, text="Select Role:")
    label_role.pack(pady=10)
    role_var = ctk.StringVar(value="")  # Default role is customer

    role_dropdown = ctk.CTkComboBox(register_window, values=["admin", "customer"], variable=role_var)
    role_dropdown.pack(pady=5)

    # Registration Logic
    def register():
        username = entry_username_reg.get()
        password = entry_password_reg.get()
        role = role_var.get()

        if not username or not password or not role:
            messagebox.showwarning("Input Error", "Please fill in all fields!")
            return

        try:
            db = connect_db()
            if not db:
                return
            cursor = db.cursor()

            # Insert new user into the database
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
            db.commit()  # Commit the changes

            messagebox.showinfo("Register", "Registration Successful!")
            register_window.destroy()  # Close the registration window

            cursor.close()
            db.close()
        except Exception as e:
            messagebox.showerror("Registration Error", f"An error occurred during registration: {e}")

    # Register Button
    register_button = ctk.CTkButton(register_window, text="Register", command=register)
    register_button.pack(pady=20)


# Main window setup
root = ctk.CTk()
root.title("Pharmacy Management System - Login")
root.geometry("800x600")

try:
    bg_image = Image.open("pharmacy management system.png")
    bg_image = bg_image.resize((1400, 1200), Image.LANCZOS)
    bg_ctk_image = ctk.CTkImage(bg_image, size=(1400, 1200))
    root.bg_image = bg_ctk_image
    bg_label = ctk.CTkLabel(root, image=root.bg_image, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print("Error loading background image:", e)

title_label = ctk.CTkLabel(root, text="PHARMACY MANAGEMENT SYSTEM", font=("Times New Roman", 24, "bold"), text_color="#333333")
title_label.pack(pady=(30, 10))

form_frame = ctk.CTkFrame(root, width=300, height=320, corner_radius=15)
form_frame.place(relx=0.5, rely=0.5, anchor="center")

login_label = ctk.CTkLabel(form_frame, text="Login", font=("Arial", 18, "bold"), text_color="#333333")
login_label.pack(pady=(20, 10))


username_label = ctk.CTkLabel(form_frame, text="Username:", font=("Arial", 12), text_color="#333333")
username_label.pack(pady=(10, 5))
entry_username = ctk.CTkEntry(form_frame, width=200, corner_radius=10)
entry_username.pack(pady=5)

password_label = ctk.CTkLabel(form_frame, text="Password:", font=("Arial", 12), text_color="#333333")
password_label.pack(pady=(10, 5))
entry_password = ctk.CTkEntry(form_frame, width=200, corner_radius=10, show="*")
entry_password.pack(pady=5)

login_button = ctk.CTkButton(form_frame, text="Login", width=150, height=32, corner_radius=10, fg_color="#4CAF50", hover_color="#45A049", command=login)
login_button.pack(pady=(20, 10))

register_button = ctk.CTkButton(form_frame, text="Register", width=150, height=32, corner_radius=10, fg_color="#2196F3", hover_color="#1E88E5", command=open_register_window)
register_button.pack(pady=(10, 10))

# Start the event loop
root.mainloop()
