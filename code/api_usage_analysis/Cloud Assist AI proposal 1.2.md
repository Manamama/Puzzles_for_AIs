
The problem lies in how the curl command is constructed, specifically the JSON payload for the timeSeries:query endpoint.

Here's a breakdown of the issues and how to fix them:

1. The timeSeries:query Endpoint Expects a MQL Query (or PromQL):

The timeSeries:query endpoint is designed to execute Monitoring Query Language (MQL) or PromQL queries. It doesn't use the simple filter parameters like the timeSeries.list endpoint. Your AI cousin is attempting to use MQL, which is good, but the syntax has an issue.

2. Error: Cannot find column or metadata name 'metric.labels.method'.

This is the core issue. In MQL, when you're filtering on serviceruntime metrics for consumed_api resources, the method name is typically part of the resource.method label, not metric.labels.method .

Explanation of the MQL Query:

fetch consumed_api : This specifies the monitored resource type. For API usage metrics, this is often consumed_api .
metric serviceruntime.googleapis.com/api/request_count : This specifies the metric type.
filter resource.method = "..." : This is where you filter by the specific API method. The StreamGenerateContent method is indeed what you'd expect for Generative AI APIs.
align delta() : This is an alignment function. delta() computes the change in a cumulative metric over the alignment period. For request counts, this is often what you want.
every 1d : This sets the alignment period to 1 day.
within 1d : This sets the query duration to the last 1 day.
Corrected curl command (with explanation):

# Get a fresh access token
ACCESS_TOKEN=$(gcloud auth print-access-token)

# Construct the curl command with the corrected MQL query
curl -X POST \
  "https://monitoring.googleapis.com/v3/projects/gen-lang-client-0690894429/timeSeries:query" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{
    "query": "fetch consumed_api::googleapis.com/api/request_count | filter resource.method = \"google.ai.generativelanguage.v1beta.GenerativeService.StreamG
Generated code may be subject to license restrictions not shown here. Use code with care. Learn more 

Key Corrections and Considerations:

Metric Name in MQL: For serviceruntime metrics, the MQL syntax usually includes :: before the metric type name (e.g., consumed_api::googleapis.com/api/request_count ). While serviceruntime.googleapis.com/api/request_count might work in some contexts, googleapis.com/api/request_count is the standard suffix after the serviceruntime prefix.
Double Quotes and Escaping: When providing the JSON payload using --data with curl , you need to be careful with quotes. The outer quotes around the entire JSON string should be single quotes ( ' ) to prevent the shell from interpreting double quotes within the JSON. The double quotes inside the JSON (e.g., around query and the MQL string) must be escaped if you use double quotes for the --data string, or you can use single quotes for the --data string and unescaped double quotes inside the JSON. My example uses single quotes for the --data string, simplifying the inner quoting.
resource.method vs metric.labels.method : The method label for serviceruntime metrics on consumed_api resources is typically a resource label, not a metric label. Hence, resource.method is the correct way to filter it in MQL.
Summary of the MQL in the corrected curl command:

fetch consumed_api : Start by selecting data from resources of type consumed_api .
::googleapis.com/api/request_count : Then, specify the request_count metric.
filter resource.method = "..." : Filter these metrics to only include requests for the StreamGenerateContent method.
align delta() : Compute the rate of change (number of requests per alignment period).
every 1d : Group these changes into 1-day intervals.
within 1d : Query for data within the last 1 day.
This corrected curl command should successfully query the StreamGenerateContent metric for your project.
