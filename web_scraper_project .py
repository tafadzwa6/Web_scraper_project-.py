import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from logging.handlers import RotatingFileHandler
import schedule
import time
from datetime import datetime
import re

# Logging setup
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = RotatingFileHandler('scraper.log', maxBytes=1000000, backupCount=5)
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# Constants
BASE_URL = "https://vacancymail.co.zw"
JOBS_LIST_URL = f"{BASE_URL}/jobs/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def clean_text(text):
    """Cleans extra spaces from text."""
    return re.sub(r'\s+', ' ', text).strip()

def fetch_jobs():
    """Fetches job listings from the website."""
    logger.info("Opening site and fetching job listings...")
    try:
        response = requests.get(JOBS_LIST_URL, headers=HEADERS)
        response.raise_for_status()  # will raise an HTTPError if the status is 4xx/5xx
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Update the selector if the website structure changed
    job_cards = soup.select("div.job-listing-details")[:10]  # limit to the first 10 jobs

    if not job_cards:
        logger.warning("No job cards found. Check the website structure.")
        return []

    jobs = []

    for card in job_cards:
        try:
            title_tag = card.find("h3", class_="job-listing-title")
            company_tag = card.find("h4", class_="job-listing-company")
            description_tag = card.find("p", class_="job-listing-text")

            location = "N/A"
            expiry = "N/A"
            for li in card.find_all("li"):
                if "icon-material-outline-location-on" in str(li):
                    location = clean_text(li.get_text())
                elif "icon-material-outline-access-time" in str(li):
                    expiry = clean_text(li.get_text()).replace("Expires", "").strip()

            jobs.append({
                'Job Title': title_tag.get_text(strip=True) if title_tag else "N/A",
                'Company': company_tag.get_text(strip=True) if company_tag else "N/A",
                'Location': location,
                'Expiry Date': format_date(expiry),
                'Job Description': description_tag.get_text(strip=True) if description_tag else "N/A",
                'Scraped At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        except Exception as e:
            logger.warning(f"Error parsing job card: {e}")

    return jobs

def format_date(date_string):
    """Formats date string to a standard format."""
    try:
        return datetime.strptime(date_string, "%d %b %Y").strftime("%Y-%m-%d")
    except ValueError:
        return date_string  # return original string if format is incorrect

def save_to_csv(jobs, filename="scraped_data.csv"):
    """Saves job data to a CSV file."""
    try:
        df = pd.DataFrame(jobs)
        df.drop_duplicates(inplace=True)  # drop any duplicate rows
        df.to_csv(filename, index=False)
        logger.info(f"Saved {len(df)} job listings to {filename}")
    except Exception as e:
        logger.error(f"Failed to save data: {e}")

def job():
    """Scrapes job data and saves to CSV."""
    logger.info("Starting scraping task...")
    jobs = fetch_jobs()
    if jobs:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scraped_data_{timestamp}.csv"
        save_to_csv(jobs, filename)
    else:
        logger.warning("No jobs scraped.")

def run_scheduler(interval='daily'):
    """Runs the scraper on a scheduled basis."""
    if interval == 'hourly':
        schedule.every().hour.do(job)
    else:
        schedule.every().day.at("09:00").do(job)

    logger.info(f"Scheduler started with interval: {interval}")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="VacancyMail Job Scraper")
    parser.add_argument('--schedule', choices=['daily', 'hourly'], help='Run scraper on schedule')
    args = parser.parse_args()

    if args.schedule:
        run_scheduler(args.schedule)
    else:
        job()