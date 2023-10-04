# Simple set up environment config for notebooks.
# Potential to use an object for injection to methods in the future.

import os
import mdsisclienttools.auth.TokenManager as ProvenaAuth
# Provena config - replace with your Provena instance endpoints

# Read the following from .env files or environment variables

PROVENA_DOMAIN = os.getenv('PROVENA_DOMAIN')
KC_ENDPOINT = os.getenv('KC_ENDPOINT')
STAGE = os.getenv('STAGE')


registry_endpoint = "https://registry-api.{}".format(PROVENA_DOMAIN)
provenance_endpoint = "https://prov-api.{}".format(PROVENA_DOMAIN)
data_store_endpoint = "https://data-api.{}".format(PROVENA_DOMAIN)
job_endpoint =  "https://job-api.{}".format(PROVENA_DOMAIN)

# sets up auth connections - could potentially open browser window if not signed
# in recently - caches in .tokens.json - ensure this is included in gitignore
provena_auth = ProvenaAuth.DeviceFlowManager(
    stage=STAGE,
    keycloak_endpoint=KC_ENDPOINT
)

# expose the get auth function which is used for provena methods 
get_auth = provena_auth.get_auth