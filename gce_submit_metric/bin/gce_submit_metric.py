import argparse
from gce_submit_metric.monitoring import GCEMonitoringClient


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='A simple script to submit metrics to GCP\'s Stackdriver.'
    )
    parser.add_argument('--metric', required=True, type=str, help='Name of metric (string)')
    parser.add_argument('--value', required=True, type=int, help='Value of metric (integer)')
    args = parser.parse_args()

    client = GCEMonitoringClient()
    client.write_time_series(args.metric, args.value)


if __name__ == '__main__':
    main()
