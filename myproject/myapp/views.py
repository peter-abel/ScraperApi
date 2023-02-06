from django.shortcuts import render

# Create your views here.
import requests
from bs4 import BeautifulSoup
import pandas as pd
from django.http import HttpResponse

def scrape_indeed(request):
    # Scrape the data from indeed.com
    URL = "https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start=10"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    results = soup.find(id='resultsCol')
    job_elems = results.find_all('div', class_='jobsearch-SerpJobCard')
    
    # Extract the relevant information for each job posting
    job_titles = []
    companies = []
    locations = []
    for job_elem in job_elems:
        title_elem = job_elem.find('h2', class_='title')
        company_elem = job_elem.find('span', class_='company')
        location_elem = job_elem.find('div', class_='recJobLoc')
        if None in (title_elem, company_elem, location_elem):
            continue
        job_titles.append(title_elem.text.strip())
        companies.append(company_elem.text.strip())
        locations.append(location_elem['data-rc-loc'].strip())

    # Save the extracted information to a CSV file
    df = pd.DataFrame({'Job Title': job_titles,
                       'Company': companies,
                       'Location': locations})
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="indeed_jobs.csv"'
    df.to_csv(path_or_buffer=response, index=False)
    return response
