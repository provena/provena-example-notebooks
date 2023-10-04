from mdsisclienttools.auth.TokenManager import BearerAuth
import requests
from typing import Dict, Any, Optional

from registry import check_response

def register_dataset(datastore_endpoint: str, dataset_metadata: Dict[str, Any], auth: BearerAuth) -> Dict[str, Any]:
    postfix = "/register/mint-dataset"
    endpoint = datastore_endpoint + postfix
    print(f"Registering dataset with metadata: {dataset_metadata}...")
    response = requests.post(url=endpoint, json=dataset_metadata, auth=auth)
    check_response(response=response, status_check=True)
    return response.json()


def update_dataset(datastore_endpoint: str, dataset_id: str, updated_metadata: Dict[str, Any], reason: str,  auth: BearerAuth) -> Dict[str, Any]:
    postfix = "/register/update-metadata"
    endpoint = datastore_endpoint + postfix
    print(f"Updating dataset with metadata: {updated_metadata}...")
    params = {"handle_id": dataset_id, "reason": reason}
    response = requests.post(url=endpoint, json=updated_metadata, params=params, auth=auth)
    check_response(response=response, status_check=True)
    return response.json()


def inject_references(metadata: Dict[str, Any], record_creator: str, publisher: str, custodian: Optional[str]=None) -> Dict[str, Any]:
    
    metadata['associations']['organisation_id'] = record_creator
    
    # Optional
    if custodian:
        metadata['associations']['data_custodian_id'] = custodian

    metadata['dataset_info']['publisher_id'] = publisher

    return metadata


def version_dataset(datastore_endpoint: str, dataset_id: str, reason: str, auth: BearerAuth) -> Dict[str, Any]:
    postfix = "/register/version"
    endpoint = datastore_endpoint + postfix
    print(f"Versioning dataset with id: {dataset_id}...")
    body = {"id": dataset_id, "reason": reason}
    response = requests.post(url=endpoint, json=body, auth=auth)
    check_response(response=response, status_check=False)
    return response.json()