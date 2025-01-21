from setuptools import setup, find_packages

setup(
    name='dash_application',
    version='0.1.0',
    packages=find_packages(include=['dash', 'dash.*']),
    install_requires=[
        'blinker==1.8.2',
        'certifi==2024.12.14',
        'charset-normalizer==3.4.1',
        'click==8.1.8',
        'dash==2.18.2',
        'dash-core-components==2.0.0',
        'dash-html-components==2.0.0',
        'dash-table==5.0.0',
        'Flask==3.0.3',
        'idna==3.10',
        'importlib_metadata==8.5.0',
        'itsdangerous==2.2.0',
        'Jinja2==3.1.5',
        'MarkupSafe==2.1.5',
        'nest-asyncio==1.6.0',
        'numpy==1.24.4',
        'packaging==24.2',
        'pandas==2.0.3',
        'plotly==5.24.1',
        'python-dateutil==2.9.0.post0',
        'pytz==2024.2',
        'requests==2.32.3',
        'retrying==1.3.4',
        'six==1.17.0',
        'tenacity==9.0.0',
        'typing_extensions==4.12.2',
        'tzdata==2024.2',
        'urllib3==2.2.3',
        'Werkzeug==3.0.6',
        'zipp==3.20.2'
    ],
    entry_points={
        'console_scripts': [
            'run-dash-app=dash.dash_application:main',
        ],
    },
)
