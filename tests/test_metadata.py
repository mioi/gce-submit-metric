"""Tests for the GCP Metadata module."""

import json
import unittest

from mock import call, patch

from gce_submit_metric.metadata import _get_instance, GCEMetadata

FAKE_METADATA = """
{
  "unique_id": "12345678",
  "name": "gce-instance-foo",
  "zone": "eu-southeast-9"
}
"""


@patch('gce_submit_metric.metadata.requests', autospec=True, spec_set=True)
def test_get_instance(mock_requests):
    _get_instance('id')
    assert mock_requests.mock_calls == [
        call.get(
            'http://metadata.google.internal/computeMetadata/v1/instance/id',
            headers={'Metadata-Flavor': 'Google'})
    ]


@patch(
    'gce_submit_metric.metadata._get_instance', autospec=True, spec_set=True)
def test_gce_metadata(mock_get_instance):
    fake_metadata = json.loads(FAKE_METADATA)

    metadata = GCEMetadata()

    mock_get_instance('id').return_value = fake_metadata['unique_id']
    assert metadata.unique_id() == '12345678'
    mock_get_instance('name').return_value = fake_metadata['name']
    assert metadata.name() == 'gce-instance-foo'
    mock_get_instance('zone').split('/')[-1].return_value = fake_metadata[
        'zone']
    assert metadata.zone() == 'eu-southeast-9'
