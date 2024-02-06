import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3
import csv
import pandas as pd
from inventory_window import InventoryWindow
from dilution_calculator_window import DilutionCalculatorWindow

class BotanicalApp:
    def __init__(self, master):
        self.master = master
        master.title("Botanical App")

        # Set the size of the main window
        master.geometry("850x400")  # Increased width to accommodate the new frame

        # Create three frames to organize the layout
        self.left_frame = tk.Frame(master)
        self.left_frame.pack(side=tk.LEFT, padx=30, pady=5)

        self.center_frame = tk.Frame(master)
        self.center_frame.pack(side=tk.LEFT, padx=30, pady=5)

        self.right_frame = tk.Frame(master)
        self.right_frame.pack(side=tk.RIGHT, padx=35, pady=5)

        # Botanical List on the Left
        self.botanical_label = tk.Label(self.left_frame, text="Botanical List")
        self.botanical_label.pack()

        self.botanical_listbox = tk.Listbox(self.left_frame, selectmode=tk.MULTIPLE, height=15, width=40)
        self.botanical_listbox.pack()

        self.refresh_botanical_button = tk.Button(self.left_frame, text="Refresh Botanical List", command=self.refresh_botanical_list, width=20)
        self.refresh_botanical_button.pack()

        self.add_botanical_button = tk.Button(self.left_frame, text="Add Botanical", command=self.add_botanical, width=20)
        self.add_botanical_button.pack()

        self.delete_botanical_button = tk.Button(self.left_frame, text="Delete Botanical", command=self.delete_botanical, width=20)
        self.delete_botanical_button.pack()

        # Recipe List in the Center
        self.recipe_label = tk.Label(self.center_frame, text="Recipe List")
        self.recipe_label.pack()

        self.recipe_listbox = tk.Listbox(self.center_frame, selectmode=tk.SINGLE, height=15, width=40)  # Adjusted width
        self.recipe_listbox.pack()

        self.refresh_recipe_button = tk.Button(self.center_frame, text="Refresh Recipe List", command=self.refresh_recipe_list, width=20)
        self.refresh_recipe_button.pack()

        self.create_recipe_button = tk.Button(self.center_frame, text="Create Recipe", command=self.create_recipe, width=20)
        self.create_recipe_button.pack()

        self.delete_recipe_button = tk.Button(self.center_frame, text="Delete Recipe", command=self.delete_recipe, width=20)
        self.delete_recipe_button.pack()

        # Database setup
        self.conn = sqlite3.connect("botanical_app.db")
        self.create_table()

        # Initialize the listboxes
        self.refresh_botanical_list()
        self.refresh_recipe_list()

        # Button to open the inventory window on the right
        self.inventory_button = tk.Button(self.right_frame, text="Open Inventory", command=self.open_inventory_window, width=35)
        self.inventory_button.pack(pady=(20, 20))

        self.dilution_calculator_button = tk.Button(self.right_frame, text="Alcohol Dilution Calculator", command=self.open_dilution_calculator, width=35)
        self.dilution_calculator_button.pack(pady=(20, 20))

        self.save_to_csv_button = tk.Button(self.right_frame, text="Save to CSV", command=self.save_data_to_csv,width=35)
        self.save_to_csv_button.pack(pady=(20, 20))

    def save_to_csv(self, data, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(data)

    def refresh_botanical_list(self):
        # Refresh the listbox with botanicals from the database
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM botanicals")
            botanicals = cursor.fetchall()

        self.botanical_listbox.delete(0, tk.END)
        for botanical in botanicals:
            self.botanical_listbox.insert(tk.END, botanical[1])

    def refresh_recipe_list(self):
        # Refresh the listbox with recipes from the database
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM recipes")
            recipes = cursor.fetchall()

        self.recipe_listbox.delete(0, tk.END)
        for recipe in recipes:
            self.recipe_listbox.insert(tk.END, f"{recipe[1]} - Ingredients: {recipe[2]}")

    def add_botanical(self):
        # Add a new botanical to the database
        name = simpledialog.askstring("Input", "Enter Botanical Name:")
        if name:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO botanicals (name) VALUES (?)", (name,))
            self.refresh_botanical_list()

    def create_recipe(self):
        selected_indices = self.botanical_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one botanical.")
            return

        selected_botanicals = [self.botanical_listbox.get(idx) for idx in selected_indices]
        recipe_name = simpledialog.askstring("Input", "Enter Recipe Name:")
        if recipe_name:
            ingredients = ", ".join(selected_botanicals)
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO recipes (name, ingredients) VALUES (?, ?)", (recipe_name, ingredients))
            messagebox.showinfo("Success", "Recipe created successfully.")
            self.refresh_recipe_list()

    def delete_botanical(self):
        selected_index = self.botanical_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a botanical to delete.")
            return

        botanical_name = self.botanical_listbox.get(selected_index)
        confirmation = messagebox.askyesno("Confirmation", f"Do you want to delete the botanical: {botanical_name}?")
        if confirmation:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM botanicals WHERE name=?", (botanical_name,))
            self.refresh_botanical_list()

    def delete_recipe(self):
        selected_index = self.recipe_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a recipe to delete.")
            return

        recipe_id = selected_index[0] + 1  # Adding 1 because recipe IDs start from 1 in the database
        confirmation = messagebox.askyesno("Confirmation", "Do you want to delete the selected recipe?")
        if confirmation:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM recipes WHERE id=?", (recipe_id,))
            self.refresh_recipe_list()

    def open_inventory_window(self):
        self.inventory_window = tk.Toplevel(self.master)
        self.inventory_window.title("Inventory")

        # Set the size of the inventory window to match the main window
        self.inventory_window.geometry(self.master.geometry())

        # Create left and right frames
        left_frame = tk.Frame(self.inventory_window)
        left_frame.pack(side=tk.LEFT, padx=20, pady=5)

        right_frame = tk.Frame(self.inventory_window)
        right_frame.pack(side=tk.RIGHT, padx=20, pady=5)

        # Fetch and display the current stock of raw materials from the database
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM inventory")
            inventory_items = cursor.fetchall()

            # Fetch and display the product list from the database
            cursor.execute("SELECT * FROM products")
            product_items = cursor.fetchall()

        # Raw Material Inventory List on the left
        inventory_left_label = tk.Label(left_frame, text="Raw Material Inventory")
        inventory_left_label.pack()

        self.inventory_listbox = tk.Listbox(left_frame, height=10, width=60)
        self.inventory_listbox.pack()

        for item in inventory_items:
            self.inventory_listbox.insert(tk.END, f"{item[1]} - Quantity: {item[2]} {item[3]}")

        # Add and Delete buttons for Inventory
        add_inventory_button = tk.Button(left_frame, text="Add to Inventory", command=self.add_inventory_item)
        add_inventory_button.pack()

        delete_inventory_button = tk.Button(left_frame, text="Delete from Inventory", command=self.delete_from_inventory)
        delete_inventory_button.pack()

        # Product List on the right
        product_right_label = tk.Label(right_frame, text="Product List")
        product_right_label.pack()

        self.product_listbox = tk.Listbox(right_frame, height=10, width=60)
        self.product_listbox.pack()

        for product in product_items:
            self.product_listbox.insert(tk.END, f"{product[1]} - Ingredients: {product[2]}")

        # Add and Delete buttons for Products
        add_product_button = tk.Button(right_frame, text="Add Product", command=self.add_product)
        add_product_button.pack()

        delete_product_button = tk.Button(right_frame, text="Delete Product", command=self.delete_product)
        delete_product_button.pack()

    def save_data_to_csv(self):
        with self.conn:
            cursor = self.conn.cursor()
            
            # Fetch data from botanicals table
            cursor.execute("SELECT * FROM botanicals")
            botanical_items = cursor.fetchall()

            # Fetch data from recipes table
            cursor.execute("SELECT * FROM recipes")
            recipe_items = cursor.fetchall()

            # Fetch data from inventory table
            cursor.execute("SELECT * FROM inventory")
            inventory_items = cursor.fetchall()

            # Fetch data from products table
            cursor.execute("SELECT * FROM products")
            product_items = cursor.fetchall()

        # Save data to a single CSV file with each table on its own sheet
        filename = 'all_data.xlsx'

        # Create a Pandas DataFrame for each table
        botanicals_df = pd.DataFrame(botanical_items, columns=["Botanicals ID", "Botanicals Name"])
        recipes_df = pd.DataFrame(recipe_items, columns=["Recipes ID", "Recipes Name", "Recipes Ingredients"])
        inventory_df = pd.DataFrame(inventory_items, columns=["Inventory ID", "Inventory Item Name", "Inventory Quantity", "Inventory Unit"])
        products_df = pd.DataFrame(product_items, columns=["Products ID", "Products Product Name", "Products Ingredients"])

        # Write each DataFrame to a different sheet in the Excel file
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            botanicals_df.to_excel(writer, sheet_name='Botanicals', index=False)
            recipes_df.to_excel(writer, sheet_name='Recipes', index=False)
            inventory_df.to_excel(writer, sheet_name='Inventory', index=False)
            products_df.to_excel(writer, sheet_name='Products', index=False)

        messagebox.showinfo("Success", f"Data saved to {filename}")

    def refresh_inventory_list(self):
        # Refresh the listbox with inventory items from the database
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM inventory")
            inventory_items = cursor.fetchall()

        self.inventory_listbox.delete(0, tk.END)
        for item in inventory_items:
            self.inventory_listbox.insert(tk.END, f"{item[1]} - Quantity: {item[2]} {item[3]}")


    # Refresh Product List
    def refresh_product_list(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM products")
            product_items = cursor.fetchall()

        self.product_listbox.delete(0, tk.END)
        for product in product_items:
            self.product_listbox.insert(tk.END, f"{product[1]} - Ingredients: {product[2]}")


    def add_product(self):
        product_name = simpledialog.askstring("Input", "Enter Product Name:")
        if product_name:
            ingredients = simpledialog.askstring("Input", "Enter Ingredients:")
            if ingredients:
                with self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute("INSERT INTO products (product_name, ingredients) VALUES (?, ?)", (product_name, ingredients))
                self.refresh_product_list()

    # Delete Product
    def delete_product(self):
        selected_index = self.product_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a product to delete.")
            return

        product_name = self.product_listbox.get(selected_index)
        # Extract product name from the displayed string
        product_name = product_name.split(" - Ingredients:")[0].strip()

        confirmation = messagebox.askyesno("Confirmation", f"Do you want to delete the product: {product_name}?")
        if confirmation:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM products WHERE product_name=?", (product_name,))
            self.refresh_product_list()

    def add_inventory_item(self):
        # Add a new item to the inventory
        name = simpledialog.askstring("Input", "Enter Item Name:")
        if name:
            quantity = simpledialog.askinteger("Input", "Enter Quantity:")
            unit = simpledialog.askstring("Input", "Enter Unit:")

            if quantity and unit:
                with self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute("INSERT INTO inventory (item_name, quantity, unit) VALUES (?, ?, ?)", (name, quantity, unit))
                self.refresh_inventory_list()

    # Delete from Inventory
    def delete_from_inventory(self):
        selected_index = self.inventory_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select an item to delete from the inventory.")
            return

        selected_item = self.inventory_listbox.get(selected_index)
        # Parse the item name from the selected string
        item_name = selected_item.split(" - Quantity:")[0].strip()

        confirmation = messagebox.askyesno("Confirmation", f"Do you want to delete {item_name} from the inventory?")
        if confirmation:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM inventory WHERE item_name=?", (item_name,))
            self.refresh_inventory_list()
    def create_table(self):
        # Create a table for botanicals if it doesn't exist
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS botanicals (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    ingredients TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    product_name TEXT NOT NULL,
                    ingredients TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY,
                    item_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit TEXT NOT NULL
                )
            """)

# Add the remaining methods (refresh_botanical_list, refresh_recipe_list, add_botanical, create_recipe, delete_botanical, delete_recipe,
# open_inventory_window, save_data_to_csv, refresh_inventory_list, refresh_product_list, add_product, delete_product) to the BotanicalApp class
