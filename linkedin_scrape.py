import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import StringVar
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters

# Global list to store scraped job data
job_data = []

def on_data(data: EventData):
    global job_data
    job_data.append({
        'title': data.title,
        'company': data.company,
        'date': data.date,
        'link': data.link,
        'description': data.description
    })

def on_error(error):
    print('[ON_ERROR]', error)

def on_end():
    print('[ON_END]')

def scrape_jobs(profession, location, experience):
    global job_data
    job_data = []

    scraper = LinkedinScraper(
        chrome_options=None,
        max_workers=1,
        slow_mo=1,
    )

    scraper.on(Events.DATA, on_data)
    scraper.on(Events.ERROR, on_error)
    scraper.on(Events.END, on_end)

    filters = QueryFilters(
        relevance=RelevanceFilters.RECENT,
        time=TimeFilters.MONTH,
        type=[TypeFilters.FULL_TIME, TypeFilters.INTERNSHIP],
        experience=None if not experience else ExperienceLevelFilters.__members__.get(experience.upper())
    )

    queries = [
        Query(
            query=profession,
            options=QueryOptions(
                locations=[location] if location else None,
                limit=10,
                filters=filters
            )
        ),
    ]

    scraper.run(queries)

    return job_data

class ScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LinkedIn Job Scraper")
        self.root.geometry("800x600")  # Set window size to 800x600
        
        # Frame for inputs
        input_frame = ttk.Frame(root)
        input_frame.pack(pady=10)

        # Profession input
        self.profession_label = ttk.Label(input_frame, text="Profession:")
        self.profession_label.grid(row=0, column=0, padx=5, pady=5)
        self.profession_entry = ttk.Entry(input_frame, width=20)  # Set width
        self.profession_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Location input
        self.location_label = ttk.Label(input_frame, text="Location:")
        self.location_label.grid(row=0, column=2, padx=5, pady=5)
        self.location_entry = ttk.Entry(input_frame, width=20)  # Set width
        self.location_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Experience input
        self.experience_label = ttk.Label(input_frame, text="Experience Level:")
        self.experience_label.grid(row=0, column=4, padx=5, pady=5)
        self.experience_combo = ttk.Combobox(input_frame, values=["Junior", "Staff", "Senior"], width=18)  # Set width and values
        self.experience_combo.grid(row=0, column=5, padx=5, pady=5)
        
        # Scrape button
        self.scrape_button = ttk.Button(root, text="Scrape", command=self.scrape)
        self.scrape_button.pack(pady=10)
        
        # Loading label
        self.loading_var = StringVar()
        self.loading_label = ttk.Label(root, textvariable=self.loading_var)
        self.loading_label.pack(pady=5)
        
        # Frame for results and scrollbar
        result_frame = ttk.Frame(root)
        result_frame.pack(pady=10, fill='both', expand=True)
        
        # Results area with vertical scrollbar
        self.results_text = tk.Text(result_frame, wrap='word', height=20, width=90)  # Increase text area size
        self.results_text.pack(side='left', fill='both', expand=True)
        
        scroll_y = ttk.Scrollbar(result_frame, orient='vertical', command=self.results_text.yview)
        scroll_y.pack(side='right', fill='y')
        
        self.results_text.config(yscrollcommand=scroll_y.set)
    
    def scrape(self):
        self.loading_var.set("Loading...")
        self.root.update_idletasks()

        profession = self.profession_entry.get()
        location = self.location_entry.get()
        experience = self.experience_combo.get()
        
        results = scrape_jobs(profession, location, experience)
        
        self.results_text.delete(1.0, tk.END)
        if results:
            for result in results:
                self.results_text.insert(tk.END, f"Title: {result['title']}\n")
                self.results_text.insert(tk.END, f"Company: {result['company']}\n")
                self.results_text.insert(tk.END, f"Date: {result['date']}\n")
                self.results_text.insert(tk.END, f"Link: {result['link']}\n")
                self.results_text.insert(tk.END, f"Description Length: {result['description']}\n")
                self.results_text.insert(tk.END, "\n" + "-"*50 + "\n")
        else:
            self.results_text.insert(tk.END, "No results found.")

        self.loading_var.set("")

if __name__ == '__main__':
    root = tk.Tk()
    app = ScraperApp(root)
    root.mainloop()
