import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import subprocess  # NEW: Needed for Notepad printing

# --- Global Variables ---
global_tax_rate = 0.15
daily_total_revenue = 0.0
daily_total_tax = 0.0
daily_merchant_count = 0
last_receipt_text = "" 

# --- Main App Function ---
def show_main_app():
    global daily_total_revenue, daily_total_tax, daily_merchant_count, last_receipt_text
    
    root = tk.Tk()
    root.title("Freeport Tax Terminal")
    root.geometry("550x850") 
    root.configure(bg="#f4f4f9")

    # --- Custom Style ---
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TLabel", background="#f4f4f9", font=("Segoe UI", 10))
    style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#003366")
    style.configure("SubHeader.TLabel", font=("Segoe UI", 10, "italic"), foreground="#666666")
    style.configure("TEntry", padding=5, font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=5)

    # --- Header ---
    header_frame = tk.Frame(root, bg="#f4f4f9")
    header_frame.pack(pady=15)
    
    ttk.Label(header_frame, text="FREEPORT OF MONROVIA", style="Header.TLabel").pack()
    ttk.Label(header_frame, text=f"Active Tax Rate: {global_tax_rate * 100:.0f}%", style="SubHeader.TLabel").pack(pady=5)

    # --- Main Form Frame ---
    form_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
    form_frame.pack(pady=10, padx=30, fill="x")

    inner_frame = tk.Frame(form_frame, bg="#ffffff")
    inner_frame.pack(padx=20, pady=15)

    # --- Merchant Details ---
    ttk.Label(inner_frame, text="Merchant ID:", background="#ffffff").grid(row=0, column=0, sticky="w", pady=5)
    entry_id = ttk.Entry(inner_frame, width=30)
    entry_id.grid(row=0, column=1, pady=5, padx=10)

    ttk.Label(inner_frame, text="Merchant Name:", background="#ffffff").grid(row=1, column=0, sticky="w", pady=5)
    entry_name = ttk.Entry(inner_frame, width=30)
    entry_name.grid(row=1, column=1, pady=5, padx=10)

    ttk.Label(inner_frame, text="Contact Number:", background="#ffffff").grid(row=2, column=0, sticky="w", pady=5)
    entry_contact = ttk.Entry(inner_frame, width=30)
    entry_contact.grid(row=2, column=1, pady=5, padx=10)

    # --- Separator ---
    ttk.Separator(inner_frame, orient='horizontal').grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

    # --- Shipment Details ---
    ttk.Label(inner_frame, text="Number of Bags:", background="#ffffff").grid(row=4, column=0, sticky="w", pady=5)
    entry_bags = ttk.Entry(inner_frame, width=30)
    entry_bags.grid(row=4, column=1, pady=5, padx=10)

    ttk.Label(inner_frame, text="Price per Bag (LRD):", background="#ffffff").grid(row=5, column=0, sticky="w", pady=5)
    entry_price = ttk.Entry(inner_frame, width=30)
    entry_price.grid(row=5, column=1, pady=5, padx=10)

    # --- Result Display ---
    result_frame = tk.Frame(root, bg="#e8f4f8", bd=1, relief="solid")
    result_frame.pack(pady=15, padx=30, fill="x")
    
    result_label = tk.Label(result_frame, text="Waiting for input...", font=("Consolas", 11), bg="#e8f4f8", justify="left", anchor="w")
    result_label.pack(padx=15, pady=15, fill="x")

    # --- Helper Function to actually print text ---
    def send_to_printer(text_to_print):
        try:
            temp_filename = "temp_receipt_to_print.txt"
            with open(temp_filename, "w") as file:
                file.write(text_to_print)
            
            # Use Notepad to print to bypass file association errors
            subprocess.run(["notepad.exe", "/p", temp_filename], shell=True)
            
            messagebox.showinfo("Printing", "Receipt sent to the default printer.")
        except Exception as e:
            messagebox.showerror("Print Error", f"Could not print: {e}")

    # --- Button Function ---
    def calculate_tax():
        global daily_total_revenue, daily_total_tax, daily_merchant_count, last_receipt_text
        try:
            merchant_id = entry_id.get()
            merchant_name = entry_name.get()
            contact = entry_contact.get()
            bags = int(entry_bags.get())
            price = float(entry_price.get())

            if bags <= 0 or price <= 0:
                messagebox.showerror("Error", "Bags and price must be greater than 0.")
                return

            current_rate = global_tax_rate
            if bags >= 10000:
                current_rate = 0.08
            elif bags >= 5000:
                current_rate = 0.10

            subtotal = bags * price
            total_tax = subtotal * current_rate
            grand_total = subtotal + total_tax

            # Update Daily Totals
            daily_total_revenue += grand_total
            daily_total_tax += total_tax
            daily_merchant_count += 1

            now = datetime.now()
            time_str = now.strftime("%Y-%m-%d %H:%M:%S")

            # Save to global variable for printing
            last_receipt_text = (
                f"=== FREEPORT OF MONROVIA ===\n"
                f"Date & Time: {time_str}\n"
                f"Merchant: {merchant_name} (ID: {merchant_id})\n"
                f"Contact: {contact}\n"
                f"-----------------------------------------\n"
                f"Base Subtotal : {subtotal:,.2f} LRD\n"
                f"Tax Rate      : {current_rate * 100:.0f}%\n"
                f"Government Tax: {total_tax:,.2f} LRD\n"
                f"GRAND TOTAL   : {grand_total:,.2f} LRD\n"
                f"=========================================\n"
            )

            result_label.config(text=last_receipt_text, fg="#003366")

            with open("receipts.txt", "a") as file:
                file.write("--- Merchant Receipt ---\n")
                file.write(last_receipt_text + "\n")
            
            # Clear form
            entry_id.delete(0, tk.END)
            entry_name.delete(0, tk.END)
            entry_contact.delete(0, tk.END)
            entry_bags.delete(0, tk.END)
            entry_price.delete(0, tk.END)
            
            entry_id.focus()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for Bags and Price.")

    # --- Print Function (For the main screen) ---
    def print_receipt():
        global last_receipt_text
        if not last_receipt_text:
            messagebox.showwarning("No Receipt", "Please calculate a receipt first before printing.")
            return
        send_to_printer(last_receipt_text)

    # --- Daily Report Function ---
    def show_daily_report():
        report_text = (
            f"Total Merchants Processed: {daily_merchant_count}\n\n"
            f"Total Tax Collected : {daily_total_tax:,.2f} LRD\n"
            f"Total Revenue (Gross): {daily_total_revenue:,.2f} LRD"
        )
        messagebox.showinfo("Daily Revenue Summary", report_text)

    # --- Search Receipt Window ---
    def open_search_window():
        search_win = tk.Toplevel(root)
        search_win.title("Search Receipt")
        search_win.geometry("450x500")
        search_win.configure(bg="#f4f4f9")

        tk.Label(search_win, text="Enter Merchant ID:", bg="#f4f4f9", font=("Segoe UI", 11)).pack(pady=10)
        search_entry = ttk.Entry(search_win, width=25, font=("Segoe UI", 12))
        search_entry.pack(pady=5)

        search_result = tk.Text(search_win, height=15, width=50, font=("Consolas", 10), bg="#ffffff", wrap="word")
        search_result.pack(pady=10)

        current_search_text = "" 

        def do_search():
            nonlocal current_search_text
            search_id = search_entry.get().strip()
            if not search_id:
                messagebox.showerror("Error", "Please enter an ID.")
                return

            search_result.delete("1.0", tk.END)
            current_search_text = "" 
            found = False
            
            try:
                with open("receipts.txt", "r") as file:
                    lines = file.readlines()
                    for i, line in enumerate(lines):
                        # Look for "(ID: 2)" instead of "ID: 2 "
                        if f"(ID: {search_id})" in line:
                            found = True
                            start = max(0, i - 2)
                            end = min(len(lines), i + 5)
                            
                            receipt_block = "".join(lines[start:end])
                            current_search_text += receipt_block + "\n"
                            
                            search_result.insert(tk.END, receipt_block + "\n")
                
                if not found:
                    search_result.insert(tk.END, f"No receipts found for ID {search_id}.")
                    current_search_text = ""
            except FileNotFoundError:
                search_result.insert(tk.END, "No receipts file found yet.")


        def print_search_result():
            nonlocal current_search_text
            if not current_search_text:
                messagebox.showwarning("No Result", "Please search for a receipt first.")
                return
            send_to_printer(current_search_text)

        btn_frame = tk.Frame(search_win, bg="#f4f4f9")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Search", command=do_search, bg="#003366", fg="white", font=("Segoe UI", 10, "bold"), width=10).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Print Result", command=print_search_result, bg="green", fg="white", font=("Segoe UI", 10, "bold"), width=10).grid(row=0, column=1, padx=5)


    # --- Action Buttons Frame ---
    action_frame = tk.Frame(root, bg="#f4f4f9")
    action_frame.pack(pady=5)

    calc_button = ttk.Button(action_frame, text="CALCULATE & SAVE", command=calculate_tax)
    calc_button.grid(row=0, column=0, padx=10, ipadx=10, ipady=5)

    print_button = tk.Button(action_frame, text="PRINT RECEIPT", command=print_receipt, bg="#003366", fg="white", font=("Segoe UI", 10, "bold"), pady=5)
    print_button.grid(row=0, column=1, padx=10)

    # --- Bottom Admin Buttons Frame ---
    admin_frame = tk.Frame(root, bg="#f4f4f9")
    admin_frame.pack(pady=10)

    report_btn = tk.Button(admin_frame, text="View Daily Revenue", command=show_daily_report, bg="#e6b800", fg="black", font=("Segoe UI", 9, "bold"))
    report_btn.grid(row=0, column=0, padx=10)

    search_btn = tk.Button(admin_frame, text="Search Receipts", command=open_search_window, bg="#cccccc", font=("Segoe UI", 9))
    search_btn.grid(row=0, column=1, padx=10)

    root.mainloop()

# --- Login Window Setup ---
login_window = tk.Tk()
login_window.title("System Locked")
login_window.geometry("400x300")
login_window.configure(bg="#003366")

tk.Label(login_window, text="=== SYSTEM LOCKED ===", bg="#003366", fg="white", font=("Segoe UI", 16, "bold")).pack(pady=30)

tk.Label(login_window, text="Enter Admin PIN:", bg="#003366", fg="white", font=("Segoe UI", 11)).pack()
entry_pin = ttk.Entry(login_window, show="*", width=20, font=("Segoe UI", 14))
entry_pin.pack(pady=10)

def check_login():
    pin = entry_pin.get()
    if pin == "2026":
        login_window.destroy()
        ask_rate()
    else:
        messagebox.showerror("Access Denied", "Incorrect PIN.")

def ask_rate():
    global global_tax_rate
    rate_window = tk.Tk()
    rate_window.title("Admin Setup")
    rate_window.geometry("400x300")
    rate_window.configure(bg="#f4f4f9")

    tk.Label(rate_window, text="Access Granted!", bg="#f4f4f9", fg="green", font=("Segoe UI", 14, "bold")).pack(pady=20)
    tk.Label(rate_window, text="Enter today's Tax Rate (eg. 15 for 15%):", bg="#f4f4f9", font=("Segoe UI", 10)).pack()
    
    entry_rate = ttk.Entry(rate_window, width=15, font=("Segoe UI", 12))
    entry_rate.pack(pady=10)

    def apply_rate():
        global global_tax_rate
        try:
            new_rate = float(entry_rate.get()) / 100.0
            global_tax_rate = new_rate
            rate_window.destroy()
            show_main_app()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def skip_rate():
        rate_window.destroy()
        show_main_app()

    tk.Button(rate_window, text="Apply New Rate", command=apply_rate, bg="#003366", fg="white", font=("Segoe UI", 10, "bold"), width=20).pack(pady=5)
    tk.Button(rate_window, text="Skip (Use 15%)", command=skip_rate, bg="#cccccc", font=("Segoe UI", 10), width=20).pack(pady=5)

    rate_window.mainloop()

login_button = tk.Button(login_window, text="UNLOCK SYSTEM", command=check_login, bg="#00cc66", fg="white", font=("Segoe UI", 12, "bold"), width=15, pady=5)
login_button.pack(pady=20)

login_window.mainloop()