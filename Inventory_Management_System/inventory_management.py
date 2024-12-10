import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class InventoryManagementSystem:
    def __init__(self, root):
        self.low_stock_button = None
        self.root = root
        self.root.title("Inventory Management System")
        self.inventory_file = "inventory.json"
        self.users_file = "users.json"
        self.current_user = None

        self.load_users()
        self.load_inventory()

        self.create_widgets()

    def create_widgets(self):
        # Login Frame
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2)

        # Inventory Frame
        self.inventory_frame = tk.Frame(self.root)

        self.product_label = tk.Label(self.inventory_frame, text="Product Name:")
        self.product_label.grid(row=0, column=0)
        self.product_entry = tk.Entry(self.inventory_frame)
        self.product_entry.grid(row=0, column=1)

        self.quantity_label = tk.Label(self.inventory_frame, text="Quantity:")
        self.quantity_label.grid(row=1, column=0)
        self.quantity_entry = tk.Entry(self.inventory_frame)
        self.quantity_entry.grid(row=1, column=1)

        self.add_button = tk.Button(self.inventory_frame, text="Add Product", command=self.add_product)
        self.add_button.grid(row=2, column=0)

        self.edit_button = tk.Button(self.inventory_frame, text="Edit Product", command=self.edit_product)
        self.edit_button.grid(row=2, column=1)

        self.delete_button = tk.Button(self.inventory_frame, text="Delete Product", command=self.delete_product)
        self.delete_button.grid(row=2, column=2)

        self.view_button = tk.Button(self.inventory_frame, text="View Inventory", command=self.view_inventory)
        self.view_button.grid(row=3, columnspan=3)

        self.low_stock_button = tk.Button(self.inventory_frame, text="Low Stock Alert", command=self.low_stock_alert)
        self.low_stock_button.grid(row=4, columnspan=3)

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {"admin": "password"}  # Default user

    def load_inventory(self):
        if os.path.exists(self.inventory_file):
            with open(self.inventory_file, 'r') as f:
                self.inventory = json.load(f)
        else:
            self.inventory = {}

    def save_inventory(self):
        with open(self.inventory_file, 'w') as f:
            json.dump(self.inventory, f)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.users and self.users[username] == password:
            self.current_user = username
            self.login_frame.pack_forget()
            self.inventory_frame.pack(pady=20)
            messagebox.showinfo("Login", "Login successful!")
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    def add_product(self):
        product_name = self.product_entry.get()
        quantity = self.quantity_entry.get()

        if product_name and quantity.isdigit():
            self.inventory[product_name] = int(quantity)
            self.save_inventory()
            messagebox.showinfo("Success", f"Added {product_name} with quantity {quantity}.")
            self.product_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid product name or quantity.")

    def edit_product(self):
        product_name = self.product_entry.get()
        quantity = self.quantity_entry.get()

        if product_name in self.inventory and quantity.isdigit():
            self.inventory[product_name] = int(quantity)
            self.save_inventory()
            messagebox.showinfo("Success", f"Updated {product_name} to quantity {quantity}.")
            self.product_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Product not found or invalid quantity.")

    def delete_product(self):
        product_name = self.product_entry.get()

        if product_name in self.inventory:
            del self.inventory[product_name]
            self.save_inventory()
            messagebox.showinfo("Success", f"Deleted {product_name} from inventory.")
            self.product_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Product not found.")

    def view_inventory(self):
        inventory_list = "\n".join([f"{name}: {quantity}" for name, quantity in self.inventory.items()])
        messagebox.showinfo("Inventory", inventory_list if inventory_list else "Inventory is empty.")

    def low_stock_alert(self):
        low_stock_items = [f"{name}: {quantity}" for name, quantity in self.inventory.items() if quantity < 5]
        if low_stock_items:
            messagebox.showwarning("Low Stock Alert", "\n".join(low_stock_items))
        else:
            messagebox.showinfo("Low Stock Alert", "No low stock items.")

if __name__ == "__main__":
    root = tk.Tk()
    ims = InventoryManagementSystem(root)
    root.geometry("400x300")
    root.mainloop()