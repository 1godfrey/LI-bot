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
            title_element = job.find_element(By.CLASS_NAME, 'base-search-card__title')
            title = title_element.text.strip() if title_element else "Not Available"
            
            company_element = job.find_element(By.CLASS_NAME, 'base-search-card__subtitle')
            company = company_element.text.strip() if company_element else "Not Available"
            
            link = job.find_element(By.TAG_NAME, 'a').get_attribute('href')
            salary = "Not listed"  # LinkedIn rarely shows salary publicly
            
            # Extract job age
            try:
                job_age_element = job.find_element(By.CLASS_NAME, 'job-search-card__listdate')
                job_age = job_age_element.get_attribute('datetime') if job_age_element else "Unknown"
                if job_age != "Unknown":
                    job_age = (datetime.now() - datetime.strptime(job_age, "%Y-%m-%d")).days
                else:
                    job_age = "Unknown"
            except:
                job_age = "Unknown"
            
            # Extract applicant count
            try:
                applicant_element = job.find_element(By.CLASS_NAME, 'job-search-card__insight')
                applicants = applicant_element.text.strip() if applicant_element else "Unknown"
            except:
                applicants = "Unknown"
            
            job_data.append([company, title, salary, job_age, applicants, link])
        except Exception as e:
            print(f"Error extracting job: {e}")
    
    # Sort by most recent jobs first
    job_data.sort(key=lambda x: x[3] if isinstance(x[3], int) else 9999)
    
    driver.quit()
    
    # Save results to CSV
    timestamp = datetime.now().strftime("%Y-%m-%d")
    csv_filename = f"linkedin_jobs_{timestamp}.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name", "Job Title", "Salary Range", "Days Since Posted", "Applicants", "Link to Application"])
        writer.writerows(job_data)
    
    print(f"CSV saved: {csv_filename}")
    return csv_filename

if __name__ == "__main__":
    scrape_linkedin_jobs()
