# VacancyMail Job Scraper 🕵️‍♂️

A powerful Python-based web scraper that extracts job listings from [VacancyMail Zimbabwe](https://vacancymail.co.zw/jobs/), cleans the data, and saves it into timestamped CSV files. Schedule it to run hourly or daily, and never miss a fresh job post again.

---

## 📦 Features

- 🔎 Scrapes latest job listings (default: top 10)
- 🧹 Cleans and formats job data
- 📁 Saves output as timestamped CSV files
- 📅 Supports scheduled scraping (hourly or daily)
- 🛠️ Logs activity and errors using rotating log files
- 📆 Standardizes expiry date formatting
- 🧪 Built with error handling and modular functions for maintainability

---

## 📂 Project Structure

vacancymail_scraper/ │ ├── scraper.py # Main scraping script ├── scraper.log # Auto-generated rotating log file ├── scraped_data_*.csv # Output CSV files with scraped job data ├── README.md # You are here └── requirements.txt # Dependency list (optional, see below)

yaml
Copy
Edit

---

## 🚀 Installation & Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/vacancymail-scraper.git
   cd vacancymail-scraper
(Optional) Create a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Or manually:

bash
Copy
Edit
pip install requests beautifulsoup4 pandas schedule
⚙️ Usage
Run the scraper once:

bash
Copy
Edit
python scraper.py
Schedule it to run daily at 9AM:

bash
Copy
Edit
python scraper.py --schedule daily
Schedule it to run every hour:

bash
Copy
Edit
python scraper.py --schedule hourly
📊 Sample Output
Each run produces a CSV file like scraped_data_20250415_090000.csv containing:


Job Title	Company	Location	Expiry Date	Job Description	Scraped At
Sales Officer	TM Motors	Harare	2025-04-30	Dynamic sales...	2025-04-15 09:00:00
Accountant	GoldFinance	Bulawayo	2025-04-22	Minimum 3 yrs...	2025-04-15 09:00:00
🪵 Logging
Logs are saved in scraper.log and rotate automatically after reaching 1MB. Example:

yaml
Copy
Edit
2025-04-15 09:00:00 - INFO - Opening site and fetching job listings...
2025-04-15 09:00:02 - INFO - Saved 10 job listings to scraped_data_20250415_090000.csv
✅ TODO / Upcoming Features
 Extract full job descriptions from individual pages

 Capture tags/categories (e.g., IT, Finance, NGO)

 Save to SQLite database

 Email daily job summary

 Build a web dashboard for viewing scraped jobs

🙌 Credits
Built by [Munhuharaswi Tafadzwa
 / TM MOTORS]
Made with ❤️ and Python.

📜 License
This project is open-source and free to use under the MIT License.

yaml
Copy
Edit
