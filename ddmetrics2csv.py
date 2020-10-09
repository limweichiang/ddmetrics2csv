## Developed by Lim Wei Chiang (weichiang.lim@datadoghq.com)
## Key references for building this script:
## - Datadog Metrics API - Query timeseries points: https://docs.datadoghq.com/api/v1/metrics/#query-timeseries-points

from time import time
from datetime import datetime
import argparse
import sys
import json
import re

# Ensure non-system modules are available, or bail.
try:
  import datadog
except Exception as e:
  print(str(type(e)) + ": " + str(e), file=sys.stderr)
  exit(-1)

# Collect CLI arguments
parser = argparse.ArgumentParser(description="Datadog Metrics to CSV Converter")
parser.add_argument("-i", "--api-key", required=True, help="API Key")
parser.add_argument("-p", "--app-key", required=True, help="App Key")
parser.add_argument("-q", "--query", required=True, help="Metrics Query String")
parser.add_argument("-s", "--start-time", help="Start time for metrics collection in YYYY-MM-DD-HH-MM format. [Default: 1 hour before end time]")
parser.add_argument("-e", "--end-time", help="End time for metrics collection in YYYY-MM-DD-HH-MM format. [Default: Now]")
parser.add_argument("-o", "--output-file", help="Filename to write CSV contents into. [Default: stdout]")
args = parser.parse_args()

# Assign arguments
dd_api_options = {'api_key': args.api_key, 'app_key': args.app_key}
dd_api_query = args.query

# Parse end of the metrics collection window
# Default is current time.
if(args.end_time is not None):
  try:
    metrics_end_time = datetime.strptime(args.end_time, '%Y-%m-%d-%H-%M').timestamp()
  except ValueError:
    print("Start time parsing error: '-e' or '--end-time' value must be in YYYY-MM-DD-HH-MM format", file=sys.stderr)
    exit(-1)
else:
  metrics_end_time = int(time())

# Parse start of the metrics collection window.
# Default is 1 hour before specified end time, or 1 hour ago if defaults are used for end time.
if(args.start_time is not None):
  try:
    metrics_start_time = datetime.strptime(args.start_time, '%Y-%m-%d-%H-%M').timestamp()
  except ValueError:
    print("End time parsing error: '-s' or '--start-time' value must be in YYYY-MM-DD-HH-MM format", file=sys.stderr)
    exit(-1)
else:
  metrics_start_time = metrics_end_time - 3600

# Initialize API
datadog.initialize(**dd_api_options)

# Execute Query
# Test for Error
results = datadog.api.Metric.query(start=metrics_start_time, end=metrics_end_time, query=dd_api_query)
if not results:
  print("Query error: No results received from query.", file=sys.stderr)
  exit(-1)

# Quit if we didn't successfully get results we can work with.
if (results["res_type"] != "time_series"):
  print("Response type error: Returned result type is not \"time_series\". Received type: " + results["res_type"], file=sys.stderr)
  exit(-1)
if (results["status"] != "ok"):
  print("Response status error: Query failed.", file=sys.stderr)
  exit(-1)

# Final output. Either print this or write this.
output = ""

# First iteration flag: Used to determine whether to print column headers.
first_iteration = True

# Iterate through each returned result
for series_iter in results["series"]:
  header_row_head = ""
  header_row_tail = ""
  data_row_head = ""
  data_row_tail = ""

  for series_key,series_val in sorted(series_iter.items()):
    # Skip if this contains the list of all datapoints
    if(series_key != "pointlist"):
      # The header should be equivalent between each series. Skip after first series.
      if(first_iteration == True):

        # Process "unit" as a special case; it is a sub-dictionary describing the pointlist values.
        if(series_key == "unit"):
          for unit_key,unit_val in sorted(series_val[0].items()):
            header_row_tail = header_row_tail + "unit_" + str(unit_key) + ';'
        else:
          header_row_head = header_row_head + series_key + ";"

      # Each series has its own unique data, we'll compile that for the row.
      # Process "unit" as a special case; it is a sub-dictionary describing the pointlist values.
      if(series_key == "unit"):
        for unit_key,unit_val in sorted(series_val[0].items()):
          data_row_tail = data_row_tail + str(unit_val) + ';'
      else:
        data_row_head = data_row_head + str(series_val) + ";"
  
  # Print column headers on based on first series.
  if(first_iteration == True):
    header_row = header_row_head + "datapoint_time;datapoint_data;" + header_row_tail
    
    # Remove trailing delimiter
    header_row = re.sub('\;$', '', header_row)
    
    output = output + header_row + '\n'
    
    # Disable flag after first series, we don't need to keep building the same column headers
    first_iteration = False

  # Harvest and get every datapoint time and value
  for datapoint in series_iter["pointlist"]:
    data_row = data_row_head + str(datapoint[0]) + ';' + str(datapoint[1]) + ';' + data_row_tail
    
    # Remove trailing delimiter
    data_row = re.sub('\;$', '', data_row)
    
    output = output + data_row + '\n'

# Write to file if requested, else printout on stdio.
if(args.output_file is not None):
  try:
    outfile = open(args.output_file, 'w')
    outfile.write(output)
    outfile.close()
  except Exception as err:
    print("File output error:" + str(err), file=sys.stderr)
    exit(-1)
else:
  print(output, end="")
