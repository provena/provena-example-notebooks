from mdsisclienttools.auth.TokenManager import BearerAuth
import requests
from typing import Dict, Any


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
    print(f"Fetching from registry, id: {id}...")
    params = {"id": id}

    # Make request and validate response
    response = requests.get(url=endpoint, params=params, auth=auth)
    check_response(response=response, status_check=True)

    # Return the item from the response
    return response.json()["item"]


def generic_post(endpoint: str, data: Any, auth: BearerAuth) -> Dict[str, Any]:
    print(f"Fetching from registry using post")

    # Make request and validate response
    response = requests.post(endpoint, json=data, auth=auth)
    check_response(response=response, status_check=True)

    # Return the item from the response
    return response.json()


def fetch_dataset(registry_endpoint: str, id: str, auth: BearerAuth) -> Dict[str, Any]:
    postfix = "/registry/entity/dataset/fetch"
    endpoint = registry_endpoint + postfix
    return generic_fetch(endpoint=endpoint, id=id, auth=auth)


def fetch_organisation(registry_endpoint: str, id: str, auth: BearerAuth) -> Dict[str, Any]:
    postfix = "/registry/agent/organisation/fetch"
    endpoint = registry_endpoint + postfix
    return generic_fetch(endpoint=endpoint, id=id, auth=auth)


def fetch_person(registry_endpoint: str, id: str, auth: BearerAuth) -> Dict[str, Any]:
    postfix = "/registry/agent/person/fetch"
    endpoint = registry_endpoint + postfix
    return generic_fetch(endpoint=endpoint, id=id, auth=auth)


def fetch_model_run_workflow_template(registry_endpoint: str, id: str, auth: BearerAuth) -> Dict[str, Any]:
    postfix = "/registry/entity/model_run_workflow/fetch"
    endpoint = registry_endpoint + postfix
    return generic_fetch(endpoint=endpoint, id=id, auth=auth)


def fetch_dataset_template(registry_endpoint: str, id: str, auth: BearerAuth) -> Dict[str, Any]:
    postfix = "/registry/entity/dataset_template/fetch"
    endpoint = registry_endpoint + postfix
    return generic_fetch(endpoint=endpoint, id=id, auth=auth)



def list_datasets(registry_endpoint: str, data: Any, auth: BearerAuth) -> Dict[str, Any]:
    postfix = "/registry/entity/dataset/list"
    endpoint = registry_endpoint + postfix
    return generic_post(endpoint=endpoint, data=data, auth=auth)


def list_model_runs(registry_endpoint: str, data: Any, auth: BearerAuth) -> Dict[str, Any]:
    postfix = "/registry/activity/model_run/list"
    endpoint = registry_endpoint + postfix
    return generic_post(endpoint=endpoint, data=data, auth=auth)

def list_persons(registry_endpoint: str, data: Any, auth: BearerAuth) -> Dict[str, Any]:
    postfix = "/registry/agent/person/list"
    endpoint = registry_endpoint + postfix
    return generic_post(endpoint=endpoint, data=data, auth=auth)

def list_organisations(registry_endpoint: str, data: Any, auth: BearerAuth) -> Dict[str, Any]:
    postfix = "/registry/agent/organisation/list"
    endpoint = registry_endpoint + postfix
    return generic_post(endpoint=endpoint, data=data, auth=auth)


def list_model_run_workflow_templates(registry_endpoint: str, data: Any, auth: BearerAuth) -> Dict[str, Any]:
    postfix = "/registry/entity/model_run_workflow/list"
    endpoint = registry_endpoint + postfix
    return generic_post(endpoint=endpoint, data=data, auth=auth)


def list_dataset_templates(registry_endpoint: str, data: Any, auth: BearerAuth) -> Dict[str, Any]:
    postfix = "/registry/entity/dataset_template/list"
    endpoint = registry_endpoint + postfix
    return generic_post(endpoint=endpoint, data=data, auth=auth)
