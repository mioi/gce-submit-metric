"""Wrapper for GCE Instance Metadata"""

import requests
from requests.packages.urllib3.exceptions import SNIMissingWarning, InsecurePlatformWarning

# TODO: When we upgrade Python we can remove this
# https://urllib3.readthedocs.io/en/latest/security.html
requests.packages.urllib3.disable_warnings(SNIMissingWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

METADATA_URL = "http://metadata.google.internal/computeMetadata/v1/instance/"
METADATA_FLAVOR = {'Metadata-Flavor': 'Google'}


def _get_instance(field):
    return requests.get(METADATA_URL + field, headers=METADATA_FLAVOR).text


class GCEMetadata(object):
    def __init__(self):
        pass

    @property
    def unique_id(self):
        return _get_instance('id')

    @property
    def name(self):
        return _get_instance('name')

    @property
    def zone(self):
        return _get_instance('zone').split('/')[-1]
