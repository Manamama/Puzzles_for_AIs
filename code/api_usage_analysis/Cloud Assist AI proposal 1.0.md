How to access the current page with metrics, https://console.cloud.google.com/apis/dashboard?project=api-project-619789377388&cloudshell=true&inv=1&invt=Ab29Fw&pageState=(%22duration%22:(%22groupValue%22:%22P14D%22,%22customValue%22:null)) via some curl?
Accessing the Google Cloud Console directly via curl to retrieve the visual data from a dashboard page, like the API Dashboard, is not possible. The Google Cloud Console is a web-based user interface that renders dynamic content using JavaScript and interacts with various backend APIs. curl is a command-line tool designed for transferring data with URLs and doesn't execute JavaScript or render a full web page.

However, you can programmatically access the underlying metrics that populate the API Dashboard using Google Cloud's APIs. The API Dashboard primarily displays metrics from Cloud Monitoring.

Here's a conceptual approach to how you would interact with Google Cloud APIs to get metric data, which you could then process with curl or a client library:

Identify the Metrics: The API Dashboard displays metrics related to API usage, such as traffic, errors, and latencies. These metrics are part of the serviceruntime metrics in Cloud Monitoring.
Use Cloud Monitoring API: You would typically use the Cloud Monitoring API to query for these metrics. Specifically, you'd be looking to query time-series data.
Authentication: To make API calls, you need to authenticate. This often involves using a service account key or user credentials.
Construct the API Request: You would form an HTTP GET request to the Cloud Monitoring API's projects.timeSeries.list endpoint. The request would include:
Your project ID ( api-project-619789377388 ).
A filter specifying the metric type (e.g., metric.type="serviceruntime.googleapis.com/api/request_count" ) and potentially labels to narrow down to specific APIs.
A startTime and endTime for the duration you're interested in (similar to your "P14D" or 14 days).
An aggregation parameter to define how the data should be grouped and reduced.
Example (Conceptual curl approach for metrics, not the dashboard itself):

# This is a conceptual example and would require proper authentication setup
# and detailed understanding of Cloud Monitoring API query parameters.

ACCESS_TOKEN=$(gcloud auth print-access-token) # Get an access token

curl -X GET \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://monitoring.googleapis.com/v3/projects/api-project-619789377388/timeSeries?filter=metric.type%3D%22serviceruntime.googleapis.com%2Fapi%2Frequest_count%22&interval.endTime=$(date -u +%Y-%m-%dT%H:%M:%SZ)&interval.s
Generated code may be subject to license restrictions not shown here. Use code with care. Learn more 

Key Takeaways:

Console is a UI: The Google Cloud Console is a visual interface, not directly accessible for data extraction via simple curl commands of the URL itself.
APIs for Data: To programmatically access the data displayed in the Console, you need to use the underlying Google Cloud APIs (e.g., Cloud Monitoring API for metrics).
Authentication is Required: All API interactions require proper authentication and authorization.
Why did you choose this rating? *

Correct

Helpful

Comprehensive

Other
Conversation sharing *

I agree to share my conversation data as feedback
Data you submit as feedback can be used by Google Cloud to improve its products, subject to the GCP Terms of Service . Don't submit personal data or data that you intend to keep confidential as feedback.

Excellent. How to get that access token from `gcloud` command? (I am authenticated there etc.
You're right, if you're already authenticated with the gcloud CLI, obtaining an access token is straightforward.

You can get an access token using the following gcloud command:

gcloud auth print-access-token
Generated code may be subject to license restrictions not shown here. Use code with care. Learn more 

This command will print a short-lived access token to your terminal. You can then use this token in the Authorization: Bearer header of your curl requests to interact with Google Cloud APIs.



#Source: side panel at https://console.cloud.google.com/apis/dashboard?project=api-project-619789377388&cloudshell=true&inv=1&invt=Ab29Fw&pageState=(%22duration%22:(%22groupValue%22:%22P14D%22,%22customValue%22:null))&chat=true itself ! 
