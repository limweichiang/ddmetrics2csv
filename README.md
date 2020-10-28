# Overview

ddmetrics2csv is a tool to query the Datadog platform for metrics using API and outputs the data in comma-separated values (CSV) format.

The tool is useful for obtaining metrics for external analytics/reporting, in situations where the analytics/reporting tool does not support JSON.

For more information about the Datadog platform APIs used by the tool, you can refer to https://docs.datadoghq.com/api/v1/metrics/#query-timeseries-points

# Usage

```
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
```
# Example

This is an example with the optional arguments provided to specify the data collection window, and file name to output to.
% python3 ./ddmetrics2csv.py \
 -i <API Key redacted> \
 -p <App Key redacted> \
 -q 'avg:system.processes.number{*} by {host,process_name}' \
 -s 2020-10-01-00-00 \
 -e 2020-10-02-23-59 \
 -o process-count.csv
 
 The results of this is attached as process-count.csv
