"""Distribution Definition to submit GCE metrics to Stackdriver"""

import sys

from setuptools import setup

MOCK_VERSION = '2.0.0'
PYTEST_VERSION = '3.0.7'
PYLINT_VERSION = '1.5.5'

# Only loads pytest-runner if needed
# See "Considerations" at https://pypi.python.org/pypi/pytest-runner
NEEDS_PYTEST = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
PYTEST_RUNNER = ['pytest-runner==2.11.1'] if NEEDS_PYTEST else []


setup(
    name='gce-submit-metric',
    version='1.0.0',
    description='Submit a metric for GCE instances to Stackdriver',
    long_description='Submit a metric for GCE instances to Stackdriver',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha', 'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux', 'Programming Language :: Python',
        'Programming Language :: Python :: 2.7', 'Topic :: System :: Distributed Computing',
        'Topic :: System :: Systems Administration'
    ],
    keywords='Cloud Infrastructure',
    url='https://github.com/mioi/gce-submit-metric',
    author='Mioi Hanaoka',
    author_email='mioihanaoka@gmail.com',
    packages=['gce_submit_metric'],
    entry_points={
        'console_scripts': ["gce-submit-metric=gce_submit_metric.bin.gce_submit_metric:main"],
    },
    setup_requires=PYTEST_RUNNER,
    install_requires=[
        'google-cloud-monitoring==0.28.0',
        'requests==2.18.4',
        'mock=={}'.format(MOCK_VERSION),
        'pylint=={}'.format(PYLINT_VERSION),
        'pytest=={}'.format(PYTEST_VERSION),
        'yapf==0.16.2',
    ],
    tests_require=[
        'mock=={}'.format(MOCK_VERSION),
        'pylint=={}'.format(PYLINT_VERSION),
        'pytest=={}'.format(PYTEST_VERSION),
        'yapf==0.16.2',
    ],
    include_package_data=True,
    zip_safe=True
)
