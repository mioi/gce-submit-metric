"""Write to Stackdriver"""

from google.cloud.monitoring import Client

from .metadata import GCEMetadata


class GCEMonitoringClient(object):
    """Client for writing a metric to Stackdriver from GCE"""
    def __init__(self, monitoring_client=None):
        if monitoring_client is None:
            monitoring_client = Client()
        self.client = monitoring_client
        self.metadata = GCEMetadata()

    def write_time_series(self, name, value):
        """Write a value from this instance to StackDriver"""
        resource = self.client.resource(
            'gce_instance',
            labels={
                'instance_id': self.metadata.unique_id,
                'zone': self.metadata.zone,
            }
        )

        metric = self.client.metric(
            type_='custom.googleapis.com/%s' % name, labels={'instance_name': self.metadata.name}
        )

        self.client.write_point(metric, resource, value)
