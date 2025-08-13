from bs4 import BeautifulSoup
import requests
import time
import json
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return None

def get_full_html_with_selenium(url):
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(url)
        time.sleep(3)

        while True:
            try:
                load_more_button = driver.find_element(By.XPATH, "//button[contains(span, 'Lebih Banyak')]")
                load_more_button.click()
                print("Tombol 'Lebih Banyak' ditekan. Menunggu konten baru...")
                time.sleep(2)
            except NoSuchElementException:
                print("Semua konten sudah dimuat.")
                break

        full_html = driver.page_source
        return full_html

    finally:
        driver.quit()
        

def scrape_jobs_list(list_url):
    
    scraped_data = []
    job_data = {}

    html_content = get_full_html_with_selenium(list_url)

    if html_content is None:
        print("Could not retrieve HTML content. Exiting.")
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    container = soup.find('div', class_ = 'recommended-jobs')

    if container:

        job_cards = container.find_all('a', class_ = 'rounded-lg')

        for job_card in job_cards:

            link = job_card.get('href')

            job_title_element = job_card.find('h2')
            job_title = job_title_element.text.strip() if job_title_element else 'N/A'

            company_name_div = job_card.find('div', class_ = 'flex items-center gap-[4.6px] text-2sm lg:text-sm text-neutral-100')

            company_name = 'N/A'
            if company_name_div:
                company_name = company_name_div.find(string=True, recursive=False).strip()

            job_detail_element = job_card.find('div', class_ = 'mb-1.5 flex flex-col gap-1 lg:mb-3')
            job_type = job_detail_element.find_all('span')[0].text.strip()
            location_detail = job_detail_element.find_all('span')[1].text.strip().replace(' • ', ',').split(',')

            if len(location_detail) > 1:
                job_location = location_detail[1].strip()
                workplace_type = location_detail[0].strip()
            else:
                job_location = 'N/A'
                workplace_type = location_detail[0].strip()

            job_details = scrape_job_details(link)
            
            job_data = {
                "job_title": job_title,
                "company_name": company_name,
                "job_type": job_type,
                "workplace_type": workplace_type,
                "job_location": job_location,
                "descriptions": job_details["descriptions"],
                "requirements": job_details["requirements"]
            }
            
            scraped_data.append(job_data)
    
    with open(f'./jobs/result_{time.strftime("%Y-%m-%d")}.json', 'w') as f:
        json.dump(scraped_data, f, indent=4)    
            

def scrape_job_details(job_url):

    full_url = f'https://dealls.com{job_url}'

    html_content = get_html(full_url)
    if not html_content:
        return None

    soup = BeautifulSoup(html_content, 'html.parser')

    description_container = soup.find('div', class_='SectionWrapper_job_description__b5mOx')
    job_description = []
    if description_container:
        job_description = [li.text.strip() for li in description_container.find_all('li')]

    requirements_container = description_container.find_next_sibling('div')
    requirements = []
    if requirements_container:
        requirements = [li.text.strip() for li in requirements_container.find_all('li')]


    return {
      "descriptions": job_description,
      "requirements": requirements
    }

def main():

    url = 'https://dealls.com/?searchJob=software+engineer'

    scrape_jobs_list(url)


if __name__ == '__main__':
    main()