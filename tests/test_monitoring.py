"""Tests for the GCP Monitoring module."""

from collections import namedtuple

from google.auth.credentials import Credentials
from google.cloud.monitoring import Client
from mock import call, Mock, patch

from gce_submit_metric.monitoring import GCEMonitoringClient

FakeMetadata = namedtuple('FakeMetadata', ['unique_id', 'name', 'zone'])
FAKE_METADATA = FakeMetadata("12345678", "gce-instance-foo", "eu-southeast-9")

FAKE_METRIC = {
    "name": "z-total-connections",
    "value": "177101"
}


@patch('gce_submit_metric.monitoring.Client', autospec=True, spec_set=True)
@patch('gce_submit_metric.monitoring.GCEMetadata', autospec=True, spec_set=True)
def test_gce_monitoring_client(mock_metadata, mock_client):
    mock_metadata.return_value = FAKE_METADATA

    client = GCEMonitoringClient()
    assert client.client == mock_client.return_value
    assert client.metadata == FAKE_METADATA
    assert mock_metadata.mock_calls == [call()]
    assert mock_client.mock_calls == [call()]

@patch('google.cloud.monitoring.Client.write_point', autospec=True, spec_set=True)
@patch('gce_submit_metric.monitoring.GCEMetadata', autospec=True, spec_set=True)
def test_write_time_series(mock_metadata, mock_write_point):
    mock_credentials = Mock(autospec=True, spec=Credentials)
    mock_metadata.return_value = FAKE_METADATA
    client = Client('fake-project', mock_credentials)

    monitoring_client = GCEMonitoringClient(client)
    monitoring_client.write_time_series('z-total-connections', '177101')

    fake_resource = client.resource(
        'gce_instance',
        labels={
            'instance_id': FAKE_METADATA.unique_id,
            'zone': FAKE_METADATA.zone,
        }
    )

    fake_metric = client.metric(
        type_='custom.googleapis.com/%s' % FAKE_METRIC['name'],
        labels={'instance_name': FAKE_METADATA.name}
    )

    assert mock_metadata.mock_calls == [call()]
    assert mock_write_point.mock_calls == [
        call(client, fake_metric, fake_resource, FAKE_METRIC['value'].encode("ascii"))
    ]
    assert mock_credentials.mock_calls == []
