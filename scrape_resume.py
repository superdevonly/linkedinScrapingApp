import tkinter as tk
from tkinter import messagebox, scrolledtext
from bs4 import BeautifulSoup
import requests

def scrape_linkedin():
    name = name_entry.get()
    location = location_entry.get()
    profession = profession_entry.get()

    url = f"https://www.linkedin.com/search/results/people/?keywords={name}%20{location}%20{profession}"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Here you can extract the information from the LinkedIn page
        # and display it in the GUI or save it to a file.
        # For demonstration purposes, let's just print the HTML content.
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, soup.prettify())

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI
root = tk.Tk()
root.title("LinkedIn People Search")

# Labels
tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="Location:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="Profession:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

# Entry fields
name_entry = tk.Entry(root, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)
location_entry = tk.Entry(root, width=30)
location_entry.grid(row=1, column=1, padx=10, pady=5)
profession_entry = tk.Entry(root, width=30)
profession_entry.grid(row=2, column=1, padx=10, pady=5)

# Button
scrape_button = tk.Button(root, text="Scrape", command=scrape_linkedin)
scrape_button.grid(row=3, column=0, columnspan=2, pady=10)

# Result Text Widget
result_text = scrolledtext.ScrolledText(root, width=80, height=20)
result_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
