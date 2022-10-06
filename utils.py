def save_to_csv(data, headers, file_name):
    import csv

    with open(file_name, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


def extract_no(text):
    import re

    numbers = re.findall(r"\b\d+\b", text)
    return int(numbers[-1])


def clean_search_post_str(job_to_search):
    job_position = (
        job_to_search.replace(" ", "+") if " " in job_to_search else job_to_search
    )
    return job_position


def generate_jobserve_url(region, lang):
    url = f"https://jobserve.com/{region}/{lang}/JobListing.aspx?"
    return url


def generate_ad_url(region, company, job_position):
    company = company.replace(" ", "-") if " " in company else company
    url = f"https://{region}.indeed.com/viewjob?cmp={company}&t={job_position}"
    return url


def save_json(data, filepath):
    import json

    with open(filepath, "w") as f:
        json.dump(data, f)
