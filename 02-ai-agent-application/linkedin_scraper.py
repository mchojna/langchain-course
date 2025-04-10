import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()


def remove_empty_fields(d):
    if isinstance(d, dict):
        return {
            k: remove_empty_fields(v)
            for k, v in d.items()
            if v not in (None, "", [], {}) and remove_empty_fields(v) != {}
        }
    elif isinstance(d, list):
        return [
            remove_empty_fields(v)
            for v in d
            if v not in (None, "", [], {}) and remove_empty_fields(v) != {}
        ]
    else:
        return d


def screpe_linkedin_profile(linkedin_profile_url: str = "", mock: bool = False):
    """Scrape information from LinkedIn profile"""
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/mchojna/920d28e085132d54942222d4898c19d3/raw/0fe265968b5e02dce9243f350b45e761cddd548f/barack-obama-scrapin"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        url = "https://api.brightdata.com/datasets/v3/trigger"

        headers = {
            "Authorization": f"Bearer {os.getenv('LINKEDIN_API_KEY')}",
            "Content-Type": "application/json",
        }

        params = {"dataset_id": "gd_l1viktl72bvl7bjuj0", "include_errors": "true"}

        data = [
            {"url": f"{linkedin_profile_url}"},
        ]

        response = requests.post(url, headers=headers, params=params, json=data)

        if response.status_code == 200:
            print("Request accepted - waiting for data")
            time.sleep(5)
            snapshot_id = response.json()["snapshot_id"]

            url = f"https://api.brightdata.com/datasets/v3/progress/{snapshot_id}"
            headers = {"Authorization": f"Bearer {os.getenv('LINKEDIN_API_KEY')}"}
            response = requests.request("GET", url, headers=headers)

            while response.json()["status"] == "running":
                print("Data is not yet available")
                time.sleep(5)
                response = requests.request("GET", url, headers=headers)
            print("Data is available")

            url = f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}"
            headers = {"Authorization": f"Bearer {os.getenv('LINKEDIN_API_KEY')}"}
            response = requests.request("GET", url, headers=headers)

    data = remove_empty_fields(response.json())

    return data
