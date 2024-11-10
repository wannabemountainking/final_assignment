import re
import requests
from bs4 import BeautifulSoup
from pprint import pprint

berlin_url = "https://berlinstartupjobs.com"
weworkRemotely_url = "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term="
web3_career_url = "https://web3.career"
berlin_jobs_db = []

headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'Accept':
      'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
}



def get_berlin_job_skill_db(url, skill):
	berlin_job_db = []
	new_response = requests.get(f"{url}/skill-areas/{skill}", headers=headers)
	if skill == "engineering":
		response = requests.get(f"{url}/engineering/", headers=headers)
		soup = BeautifulSoup(response.text, 'html.parser')
		berlin_job_db = []
		job_pages = soup.find_all(class_="page-numbers")
		number_of_pages = 0
		if job_pages:
			number_of_pages = len(job_pages)
		else:
			number_of_pages = 2
		for i in range(1, number_of_pages):
			new_response = requests.get(f"{url}/engineering/page/{i}", headers=headers)

	soup = BeautifulSoup(new_response.text, "html.parser")
	jobs = soup.find_all("li", class_="bjs-jlid")
	for job in jobs:
		raw_link = job.find("a")
		title = raw_link
		link = raw_link["href"]
		company = job.find("a", class_="bjs-jlid__b").text
		job_description = re.sub("\n|\t", "", job.find("div", class_="bjs-jlid__description").text)
		job_data = dict(
			company=company,
			job_title=title,
			job_description = job_description,
			link = link
		)
		pprint(job_data)
		berlin_job_db.append(job_data)
	pprint(berlin_job_db)
	return berlin_job_db

# pprint(get_berlin_job_skill_db(berlin_url, "engineering"))

def get_web3_career_job_skill_db(url, skill):
	web3_career_url = f"{url}/{skill}-jobs"
	page_number = 0
	web3_career_jobs_db = []
	have_more_pages = True
	while have_more_pages:
		page_number += 1
		print(page_number)
		response = requests.get(f"{web3_career_url}?page={page_number}")
		soup = BeautifulSoup(response.text, "html.parser")
		pagination = soup.find("ul", class_="pagination")
		lastPage = pagination.find_all("a")[-1]["href"] == "#"
		if (pagination == None) or lastPage:
			have_more_pages = False
		jobs = soup.find_all("tr", class_="table_row")
		jobs.remove(soup.find("tr", id="sponsor_2"))
		for job in jobs:
			raw_link = job.find("a")
			link = f"{url}{raw_link["href"]}"
			title = raw_link.text
			company = job.find("h3").text
			job_description = ""
			for skill_needed in job.find_all("span", class_="my-badge"):
				job_description += f"{skill_needed.text}"
			job_data = dict(
				link=link,
				job_title=title,
				job_description=job_description,
				company=company
			)
			web3_career_jobs_db.append(job_data)
	return web3_career_jobs_db

# pprint(get_web3_career_job_skill_db(url="https://web3.career", skill="python"))

def weworkremotely_skill_db(url, skill):
	response = requests.get(f"{url}{skill}", headers=headers)
	soup = BeautifulSoup(response.text, "html.parser")
	wr_jobs_db = []
	job_items = soup.select("article ul > li")[:-1]
	for item in job_items:
		link = f"{url}{item.find_all("a", href=True)[1]['href']}"
		job_title = item.select_one("span.title").text
		job_description = item.select_one("span.region").text
		company = item.find_all("a", href=True)[1].find("span", class_="company").text
		wr_job = dict(
			link=link,
			job_title=job_title,
			job_description=job_description,
			company=company
		)
		wr_jobs_db.append(wr_job)
	pprint(wr_jobs_db)
	return wr_jobs_db
weworkremotely_skill_db(weworkRemotely_url, "python")