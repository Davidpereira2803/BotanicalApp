import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3

class InventoryWindow:
    def __init__(self, master, conn):
        self.master = master
        self.master.title("Inventory")

        # Set the size of the inventory window
        self.master.geometry("800x400")

        # Create left and right frames
        self.left_frame = tk.Frame(self.master)
        self.left_frame.pack(side=tk.LEFT, padx=20, pady=5)

        self.right_frame = tk.Frame(self.master)
        self.right_frame.pack(side=tk.RIGHT, padx=20, pady=5)

        # Initialize the database connection
        self.conn = conn

        # Fetch and display the current stock of raw materials from the database
        self.refresh_inventory_list()

        # Raw Material Inventory List on the left
        inventory_left_label = tk.Label(self.left_frame, text="Raw Material Inventory")
        inventory_left_label.pack()

        self.inventory_listbox = tk.Listbox(self.left_frame, height=10, width=60)
        self.inventory_listbox.pack()

        # Add and Delete buttons for Inventory
        add_inventory_button = tk.Button(self.left_frame, text="Add to Inventory", command=self.add_inventory_item)
        add_inventory_button.pack()

        delete_inventory_button = tk.Button(self.left_frame, text="Delete from Inventory", command=self.delete_from_inventory)
        delete_inventory_button.pack()

    def refresh_inventory_list(self):
        # Refresh the listbox with inventory items from the database
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM inventory")
            inventory_items = cursor.fetchall()

        self.inventory_listbox.delete(0, tk.END)
        for item in inventory_items:
            self.inventory_listbox.insert(tk.END, f"{item[1]} - Quantity: {item[2]} {item[3]}")

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

# Main entry point for testing
if __name__ == "__main__":
    root = tk.Tk()
    conn = sqlite3.connect("botanical_app.db")  # Connect to the database
    app = InventoryWindow(root, conn)
    root.mainloop()
