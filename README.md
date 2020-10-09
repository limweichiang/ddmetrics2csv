# ddmetrics2csv

 % python3 ddmetrics2csv.py -h
usage: ddmetrics2csv.py [-h] -i API_KEY -p APP_KEY -q QUERY [-s START_TIME]
                        [-e END_TIME] [-o OUTPUT_FILE]

Datadog Metrics to CSV Converter

optional arguments:
  -h, --help            show this help message and exit
  -i API_KEY, --api-key API_KEY
                        API Key
  -p APP_KEY, --app-key APP_KEY
                        App Key
  -q QUERY, --query QUERY
                        Metrics Query String
  -s START_TIME, --start-time START_TIME
                        Start time for metrics collection in YYYY-MM-DD-HH-MM
                        format. [Default: 1 hour before end time]
  -e END_TIME, --end-time END_TIME
                        End time for metrics collection in YYYY-MM-DD-HH-MM
                        format. [Default: Now]
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Filename to write CSV contents into. [Default: stdout]
