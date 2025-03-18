import csv
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrape_linkedin_jobs():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    linkedin_jobs_url = "https://www.linkedin.com/jobs/search/?f_TPR=r86400&f_WT=2&keywords=software%20engineer"
    driver.get(linkedin_jobs_url)
    time.sleep(5)  # Allow time for page to load
    
    jobs = driver.find_elements(By.CLASS_NAME, 'base-search-card')
    
    job_data = []
    for job in jobs:
        try:
            title = job.find_element(By.CLASS_NAME, 'base-search-card__title').text.strip()
            company = job.find_element(By.CLASS_NAME, 'base-search-card__subtitle').text.strip()
            link = job.find_element(By.TAG_NAME, 'a').get_attribute('href')
            salary = "Not listed"  # LinkedIn rarely shows salary publicly
            
            job_data.append([company, title, salary, link])
        except Exception as e:
            print(f"Error extracting job: {e}")
    
    driver.quit()
    
    # Save results to CSV
    timestamp = datetime.now().strftime("%Y-%m-%d")
    csv_filename = f"linkedin_jobs_{timestamp}.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name", "Job Title", "Salary Range", "Link to Application"])
        writer.writerows(job_data)
    
    print(f"CSV saved: {csv_filename}")
    return csv_filename

if __name__ == "__main__":
    scrape_linkedin_jobs()
