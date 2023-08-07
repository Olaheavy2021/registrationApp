import requests, json

url = "https://jsearch.p.rapidapi.com/search"
querystring = {
    "query": "remote junior product management",
    "page": "1",
    "num_pages": "3",
}
headers = {
    "X-RapidAPI-Key": "a7683e8edfmsh4388f741d2371fep198e71jsna1a7d6168705",
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
}
response = requests.get(url, headers=headers, params=querystring)
jobs = []
if response.status_code == 200:
    jobs_data = response.json()["data"]
    jobs = [
        {
            "employer_name": jobs["employer_name"],
            "employer_logo": jobs["employer_logo"],
            "job_employment_type": jobs["job_employment_type"],
            "job_title": jobs["job_title"],
            "job_apply_link": jobs["job_apply_link"],
            "job_description": jobs["job_description"],
            "job_city": jobs["job_city"],
            "job_country": jobs["job_country"],
        }
        for jobs in jobs_data
    ]

print(json.dumps(jobs_data, indent=2))
