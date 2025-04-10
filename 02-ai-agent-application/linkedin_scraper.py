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
        pass

    data = remove_empty_fields(response.json())

    return data
