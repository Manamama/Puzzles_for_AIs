To programmatically access the same metrics displayed in the Google Cloud Console at the URL `https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/metrics?...`, which shows usage metrics for the Gemini API (`generativelanguage.googleapis.com`), you can use the Google Cloud Monitoring API. The console likely displays metrics such as `serviceruntime.googleapis.com/api/request_count` or `cloudaicompanion.googleapis.com/usage/response_count` for the `generativelanguage.googleapis.com` service, aggregated daily. Below, I provide a concise Python script to query these metrics, replicating the console's functionality, with a focus on minimal code as requested.

### Approach
- **Metric to Query**: Based on the provided information and web research, the relevant metric is likely `cloudaicompanion.googleapis.com/usage/response_count`, which tracks API responses (equivalent to requests) for the Gemini API. The console may also use `serviceruntime.googleapis.com/api/request_count` for general API usage, so both are considered.
- **API**: Use the Google Cloud Monitoring API’s `timeSeries.list` method to fetch time-series data for the metric, with daily aggregation to match the console’s typical display.
- **Authentication**: Use Application Default Credentials (ADC) via `gcloud auth application-default login` for simplicity.
- **Aggregation**: Set a 24-hour alignment period with `ALIGN_DELTA` to get daily totals, mirroring the console’s aggregated view.

### Prerequisites
1. **Enable APIs**: Ensure the Cloud Monitoring API (`monitoring.googleapis.com`) is enabled in your Google Cloud project (same as `api-project-619789377388` in your URL).
   - In Google Cloud Console, go to "APIs & Services" > "Library," search for "Cloud Monitoring API," and enable it.[](https://cloud.google.com/monitoring/api/enable-api)
2. **Billing**: A billing account must be linked to the project, as Cloud Monitoring requires it, even for free-tier usage.[](https://cloud.google.com/apis/docs/monitoring)
3. **Install Library**: Install the Google Cloud Monitoring Python client library:
   ```bash
   pip install google-cloud-monitoring
   ```
4. **Authenticate**: Run the following to set up ADC:
   ```bash
   gcloud auth application-default login
   ```
5. **Project ID**: Use your project ID (`api-project-619789377388` from the URL).

### Python Code
Below is a concise Python script to fetch daily API usage for `generativelanguage.googleapis.com`, replicating the console’s metrics view:

```python
from google.cloud import monitoring_v3
from datetime import datetime, timedelta

def get_daily_gemini_usage(project_id):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)  # Last 24 hours

    # Initialize query
    query = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type = "cloudaicompanion.googleapis.com/usage/response_count"',
            "interval": {
                "start_time": start_time,
                "end_time": end_time
            },
            "aggregation": {
                "alignment_period": {"seconds": 86400},  # 24 hours
                "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_DELTA
            }
        }
    )

    # Print daily total
    for time_series in query:
        for point in time_series.points:
            print(f"Daily API requests (ending {point.interval.end_time}): {point.value.double_value}")

# Replace with your project ID
get_daily_gemini_usage("api-project-619789377388")
```

### Explanation
- **Metric Type**: Uses `cloudaicompanion.googleapis.com/usage/response_count`, which tracks Gemini API responses, as per [Monitor Gemini for Google Cloud usage](https://cloud.google.com/gemini/docs/monitor-gemini). If the console displays `serviceruntime.googleapis.com/api/request_count`, replace the metric type in the filter accordingly.[](https://cloud.google.com/apis/docs/monitoring)
- **Time Interval**: Queries the last 24 hours to get yesterday’s usage, adjustable via `timedelta`.
- **Aggregation**: `ALIGN_DELTA` with a 24-hour (86,400 seconds) alignment period ensures daily totals, matching the console’s aggregated view.
- **Output**: Prints the total number of API requests for the day, similar to the console’s metrics display (e.g., traffic or request counts).

### Alternative Metric
If the console specifically shows `serviceruntime.googleapis.com/api/request_count`, modify the filter:
```python
"filter": 'metric.type = "serviceruntime.googleapis.com/api/request_count" AND metric.labels.service = "generativelanguage.googleapis.com"'
```
This filters for Gemini API-specific requests, as `serviceruntime` metrics cover multiple services.[](https://cloud.google.com/apis/docs/monitoring)

### Notes
- **Data Availability**: Metrics may have a slight delay (a few minutes) before appearing, as noted in.[](https://cloud.google.com/iam/docs/service-account-monitoring)
- **Pagination**: If more than 10,000 data points are returned, pagination is needed. This script assumes typical usage fits within one page. For large datasets, add pagination logic using `query.next_page_token`.[](https://medium.com/google-cloud/fetching-monitoring-metrics-data-from-gcp-into-your-application-using-python-214358b0047e)
- **Error Handling**: Add try-except blocks for production use to handle authentication or API errors.
- **Console Match**: The script mirrors the console’s daily aggregated view. To verify the exact metric, check the console’s Metrics Explorer (under "Monitoring") for the metric type used in the dashboard.[](https://cloud.google.com/apis/docs/monitoring)

### Validation
To confirm the script matches the console:
1. Run the script and compare the output (daily request count) with the console’s metrics graph for the same period.
2. In the console, go to Metrics Explorer, select the `Consumed API` resource type, and choose the metric (`cloudaicompanion.googleapis.com/usage/response_count` or `serviceruntime.googleapis.com/api/request_count`) to verify data alignment.[](https://cloud.google.com/apis/docs/monitoring)

This script is the shortest, most robust way to programmatically access the same metrics as the Google Cloud Console, leveraging the official Python client library for simplicity and reliability.[](https://cloud.google.com/monitoring/docs/reference/libraries)
