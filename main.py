import json 
import requests
import time 
import logging 
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()
from pymongo.mongo_client import MongoClient

# Configure logging
logging.basicConfig(level= logging.INFO)
log = logging.getLogger(__name__)

gh_token = os.getenv('GITHUB_TOKEN')
mongo_password = os.getenv('MONGO_PASSWORD')



def time_track(start,name):
    elapsed = time.time() - start
    log.info(f"{name} took {elapsed}\n\n")

def get_github_client_headers(token):
    headers = {
        "Accept" : "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    return headers

def get_issues_from_github(token, page=1):
    start_time = time.time()
    url = f"https://api.github.com/search/issues?q=is:issue+label:good-first-issue+state:open&per_page=100&page={page}"

    gh_headers = get_github_client_headers(token)

    response = requests.get(url, headers=gh_headers)

    print(f"Received {response.status_code} for url {response.url}")
    results = response.json()
    time_track(start_time, "GitHub API")
    return results

def insert_into_file(file_name, results):
    start_time = time.time()
   
    with open (file_name, "w") as f:
        json.dump(results, f)
    time_track(start_time, f"insert into {file_name}")

def insert_into_database(mongo_client, results):
    start_time = time.time()

    db = mongo_client["github_issues"]
    issues_collection = db["issues"]
    issues_collection.insert_many(results)
    time_track(start_time, "Insert into MongoDB")

def find_good_first_issue(labels):
    for label in labels:
        if label.get("name") == "good-first-issue":
            label_url = label.get("url").replace("https://api.github.com/repos/","https://github.com/")
            label_name = label.get("name")
            return {
                "label_name": label_name,
                "label_url": label_url
            }
        
    return {
        "label_name": "", "label_url": "",
    }


def process_json(json_file):
    start_time = time.time()
    with open(json_file,"r") as f:
        data = json.load(f)
    result_data = []

    for item in data.get("items", []):
        issue_title = item.get("title", "")
        repo_name = item.get("repository_url", "").replace("https://api.github.com/repos/"," ")
        issue_url = item.get("html_url", "")
        labels_info = find_good_first_issue(item.get("labels", []))
        state = item.get("state",  "")
        locked = item.get("locked", False)
        result_entry = {
            "issue_title": issue_title, 
            "repo_name": repo_name,
            "issue_url": issue_url,
            "label_name": labels_info["label_name"], 
            "label_url":labels_info["label_url"],
            "state": state,
            "locked": locked
        }
        result_data.append(result_entry)
    time_track(start_time, f"Processed {json_file}")
    return result_data

def main():
    start_time = time.time()
    time_track(start_time, "Total execution time")

if __name__ == "__main__":
  main()