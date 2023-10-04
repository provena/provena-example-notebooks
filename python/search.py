from mdsisclienttools.auth.TokenManager import BearerAuth
import requests
from typing import Dict, Any
import registry

def check_response(response: requests.Response, status_check: bool) -> None:
    status_code = response.status_code
    if (status_code != 200):
        raise Exception(
            f"Non 200 status code in response: {status_code}. Response: {response.text}.")
    if status_check:
        status_object = response.json()["status"]
        if not status_object["success"]:
            raise Exception(
                f"200OK response but status success was false. Message: {status_object['details']}")


def generic_fetch(endpoint: str, id: str, auth: BearerAuth) -> Dict[str, Any]:
    print(f"Fetching from search API, id: {id}...")
    params = {"id": id}

    # Make request and validate response
    response = requests.get(url=endpoint, params=params, auth=auth)
    check_response(response=response, status_check=True)

    # Return the item from the response
    return response.json()["item"]


def search_dataset(search_endpoint: str, registry_endpoint: str, query: str, subtype_filter: str, record_limit: str, auth: BearerAuth) -> Dict[str, Any]:
    postfix = "/search/entity-registry"
    endpoint = search_endpoint + postfix
    
    params = {
        "query": query,
        "subtype_filter": subtype_filter,
        "record_limit": record_limit,
              }

    # Make request and validate response
    response = requests.get(url=endpoint, params=params, auth=auth)
    check_response(response=response, status_check=True)

    #iterate through each result and fetch the title
    results = response.json()["results"]
    for idx, item in enumerate(results):
        curr_dataset = registry.fetch_dataset(registry_endpoint=registry_endpoint, id=item['id'], auth=auth)
        results[idx]['dataset_metadata'] = curr_dataset


    return results


