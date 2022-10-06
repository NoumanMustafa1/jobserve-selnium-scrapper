import pause
from selenium import webdriver
from selenium.webdriver.common.by import By

# from selenium.webdriver.support.ui import Select

from static import *
from utils import save_to_csv, generate_jobserve_url, save_json


def get_driver_connection(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver


def search_for_jobs_on_jobserve(driver, job_position, city, freshness_rate=1):
    driver.find_element(By.ID, search_keywords_id).send_keys(job_position)
    try:
        driver.find_element(By.ID, search_location_id).send_keys(city)
        # day_selection = Select(driver.find_element(By.ID,"selAge").click())
        # day_selection.select_by_value(freshness_rate)
        # pause.sleep(1)
        driver.find_element(By.ID, popup_search_button).click()
        driver.find_element(By.ID, "numberSelect").click()
        pause.sleep(1)
        driver.find_element(By.ID, "lk200").click()

        return [True, "Success"]
    except Exception as e:
        return [False, f"WHEN SEARCHINH JOB EXCEPTION OCCURED:{e}"]


def get_next_page_url(driver, page_no):
    frm_element = driver.find_element(By.ID, "frm1")
    page_url = frm_element.get_attribute("action")
    url = f"{page_url}&page={page_no}"
    return url


def extract_page_posts(driver):
    posts_data = {
        "location_elements": driver.find_elements(By.ID, "summlocation"),
        "designations_elements": driver.find_elements(By.CLASS_NAME, "jobListPosition"),
        "type_elements": driver.find_elements(By.ID, "summtype"),
        "description_elements": driver.find_elements(By.CLASS_NAME, "jobListSkills"),
        "reference_elements": driver.find_elements(By.ID, "summreference"),
        "posted_date_elements": driver.find_elements(By.ID, "summposteddate"),
    }
    return posts_data


def extract_posts(driver, positon, city, region, lang):
    # total_jobs=int(driver.find_element(By.CLASS_NAME,"resultnumber").text.replace(",",""))
    # total_pages = total_jobs//20
    page_no = 1
    posts = []
    while page_no != 3:
        print(f"GETTING POSTS FROM PAGE {page_no}")
        posts_data = extract_page_posts(driver)
        for i in range(len(posts_data["designations_elements"])):
            post = {
                "designations": posts_data["designations_elements"][i].text,
                "ad url": posts_data["designations_elements"][i].get_attribute("href"),
                "location": posts_data["location_elements"][i].text,
                "type": posts_data["type_elements"][i].text,
                "description": posts_data["description_elements"][i].text,
                "reference": posts_data["reference_elements"][i].text,
                "posted date": posts_data["posted_date_elements"][i].text,
            }
            print("post:", post)
            posts.append(post)
            print("Found", len(posts))
        page_no += 1
        url = get_next_page_url(driver, page_no)
        driver = get_driver_connection(url)
    return posts


def initiaite_process(position, region="gb", lang="en", city="london"):
    url = generate_jobserve_url(region, lang)
    driver = get_driver_connection(url)
    print("searching position:", position)
    search_query_result = search_for_jobs_on_jobserve(driver, position, city)
    pages_data = extract_posts(driver, position, city, region, lang)
    save_to_csv(pages_data, HEADER, f"{position}.csv")
    driver.close()
    print("done")
