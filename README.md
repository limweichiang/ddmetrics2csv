# Overview

ddmetrics2csv is a tool to query the Datadog platform for metrics using API and outputs the data in comma-separated values (CSV) format.

The tool is useful for obtaining metrics for external analytics/reporting, in situations where the analytics/reporting tool does not support JSON.

For more information about the Datadog platform APIs used by the tool, you can refer to https://docs.datadoghq.com/api/v1/metrics/#query-timeseries-points

# Requirements

I've only developed against these requirements, so YMMV. Do raise an issue (or better, fix and send me a PR) if you encounter problems with updated libraries.
```
% pip3 freeze
certifi==2020.6.20
chardet==3.0.4
datadog==0.39.0
decorator==4.4.2
idna==2.10
requests==2.24.0
urllib3==1.25.10
```

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
```
% python3 ./ddmetrics2csv.py \
 -i <API Key redacted> \
 -p <App Key redacted> \
 -q 'avg:system.processes.number{*} by {host,process_name}' \
 -s 2020-10-01-00-00 \
 -e 2020-10-02-23-59 \
 -o example-result-process-count.csv
```
  
The result is file that looks like this:
```
aggr;attributes;display_name;end;expression;interval;length;metric;query_index;scope;start;tag_set;datapoint_time;datapoint_data;unit_family;unit_id;unit_name;unit_plural;unit_scale_factor;unit_short_name
avg;{};system.processes.number;1601654399000;avg:system.processes.number{host:i-1234567890abcdefg,process_name:php-fpm7.2};600;288;system.processes.number;0;host:i-1234567890abcdefg,process_name:php-fpm7.2;1601481600000;['host:i-1234567890abcdefg', 'process_name:php-fpm7.2'];1601481600000.0;3.0;system;20;process;processes;1.0;proc
avg;{};system.processes.number;1601654399000;avg:system.processes.number{host:i-1234567890abcdefg,process_name:php-fpm7.2};600;288;system.processes.number;0;host:i-1234567890abcdefg,process_name:php-fpm7.2;1601481600000;['host:i-1234567890abcdefg', 'process_name:php-fpm7.2'];1601482200000.0;3.0;system;20;process;processes;1.0;proc
avg;{};system.processes.number;1601654399000;avg:system.processes.number{host:i-1234567890abcdefg,process_name:php-fpm7.2};600;288;system.processes.number;0;host:i-1234567890abcdefg,process_name:php-fpm7.2;1601481600000;['host:i-1234567890abcdefg', 'process_name:php-fpm7.2'];1601482800000.0;3.0;system;20;process;processes;1.0;proc
avg;{};system.processes.number;1601654399000;avg:system.processes.number{host:i-1234567890abcdefg,process_name:php-fpm7.2};600;288;system.processes.number;0;host:i-1234567890abcdefg,process_name:php-fpm7.2;1601481600000;['host:i-1234567890abcdefg', 'process_name:php-fpm7.2'];1601483400000.0;3.0;system;20;process;processes;1.0;proc
avg;{};system.processes.number;1601654399000;avg:system.processes.number{host:i-1234567890abcdefg,process_name:php-fpm7.2};600;288;system.processes.number;0;host:i-1234567890abcdefg,process_name:php-fpm7.2;1601481600000;['host:i-1234567890abcdefg', 'process_name:php-fpm7.2'];1601484000000.0;3.0;system;20;process;processes;1.0;proc
avg;{};system.processes.number;1601654399000;avg:system.processes.number{host:i-1234567890abcdefg,process_name:php-fpm7.2};600;288;system.processes.number;0;host:i-1234567890abcdefg,process_name:php-fpm7.2;1601481600000;['host:i-1234567890abcdefg', 'process_name:php-fpm7.2'];1601484600000.0;3.0;system;20;process;processes;1.0;proc
avg;{};system.processes.number;1601654399000;avg:system.processes.number{host:i-1234567890abcdefg,process_name:php-fpm7.2};600;288;system.processes.number;0;host:i-1234567890abcdefg,process_name:php-fpm7.2;1601481600000;['host:i-1234567890abcdefg', 'process_name:php-fpm7.2'];1601485200000.0;3.0;system;20;process;processes;1.0;proc
avg;{};system.processes.number;1601654399000;avg:system.processes.number{host:i-1234567890abcdefg,process_name:php-fpm7.2};600;288;system.processes.number;0;host:i-1234567890abcdefg,process_name:php-fpm7.2;1601481600000;['host:i-1234567890abcdefg', 'process_name:php-fpm7.2'];1601485800000.0;3.0;system;20;process;processes;1.0;proc
avg;{};system.processes.number;1601654399000;avg:system.processes.number{host:i-1234567890abcdefg,process_name:php-fpm7.2};600;288;system.processes.number;0;host:i-1234567890abcdefg,process_name:php-fpm7.2;1601481600000;['host:i-1234567890abcdefg', 'process_name:php-fpm7.2'];1601486400000.0;3.0;system;20;process;processes;1.0;proc

```
