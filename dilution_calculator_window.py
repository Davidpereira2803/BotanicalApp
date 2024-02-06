import tkinter as tk
from tkinter import simpledialog, messagebox

class DilutionCalculatorWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Alcohol Dilution Calculator")

        # Labels and entry fields for user input
        initial_concentration_label = tk.Label(self.master, text="Initial Alcohol Concentration (%):")
        initial_concentration_label.grid(row=0, column=0, pady=10, padx=10, sticky=tk.E)

        initial_concentration_entry = tk.Entry(self.master)
        initial_concentration_entry.grid(row=0, column=1, pady=10, padx=10)

        initial_volume_label = tk.Label(self.master, text="Initial Solution Volume (ml):")
        initial_volume_label.grid(row=1, column=0, pady=10, padx=10, sticky=tk.E)

        initial_volume_entry = tk.Entry(self.master)
        initial_volume_entry.grid(row=1, column=1, pady=10, padx=10)

        target_concentration_label = tk.Label(self.master, text="Target Alcohol Concentration (%):")
        target_concentration_label.grid(row=2, column=0, pady=10, padx=10, sticky=tk.E)

        target_concentration_entry = tk.Entry(self.master)
        target_concentration_entry.grid(row=2, column=1, pady=10, padx=10)

        # Label to display the result
        result_label = tk.Label(self.master, text="")
        result_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Function to calculate and display the result
        def calculate_dilution():
            try:
                C1 = float(initial_concentration_entry.get())
                V1 = float(initial_volume_entry.get())
                C2 = float(target_concentration_entry.get())

                V2 = (C1 * V1) / C2

                final = V2 - V1

                result_label.config(text=f"To achieve {C2}% alcohol, add {final:.2f} ml of distilled water.")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numerical values.")

        # Button to trigger the calculation
        calculate_button = tk.Button(self.master, text="Calculate", command=calculate_dilution)
        calculate_button.grid(row=3, column=0, columnspan=2, pady=20)

# Add the remaining methods (calculate_dilution) to the DilutionCalculatorWindow class

if __name__ == "__main__":
    root = tk.Tk()
    dilution_window = DilutionCalculatorWindow(root)
    root.mainloop()
