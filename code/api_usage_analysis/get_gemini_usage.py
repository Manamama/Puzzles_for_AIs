from google.cloud import monitoring_v3
from datetime import datetime, timedelta
from google.protobuf import duration_pb2

def get_gemini_api_daily_usage(project_id: str) -> int:
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now.timestamp()
    start_time = (now - timedelta(days=1)).timestamp()

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(end_time), 'nanos': int((end_time - int(end_time)) * 10**9)},
        start_time={'seconds': int(start_time), 'nanos': int((start_time - int(start_time)) * 10**9)},
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period=duration_pb2.Duration(seconds=24 * 60 * 60),  # 24 hours
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_DELTA,
    )

    query = f'metric.type="cloudaicompanion.googleapis.com/usage/response_count"'

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=query,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    results = client.list_time_series(request=request)

    total_requests = 0
    for series in results:
        for point in series.points:
            total_requests += point.value.double_value
    return int(total_requests)

if __name__ == "__main__":
    import os
    import subprocess

    def get_gcloud_project_id():
        try:
            project_id = subprocess.check_output(["gcloud", "config", "get-value", "project"]).decode("utf-8").strip()
            return project_id
        except subprocess.CalledProcessError:
            print("Error: Could not get gcloud project ID. Please ensure gcloud CLI is installed and configured.")
            return None

    project_id = get_gcloud_project_id()
    if project_id:
        daily_usage = get_gemini_api_daily_usage(project_id)
        print(f"Gemini API requests (last 24h) for project '{project_id}': {daily_usage}")
    else:
        print("Cannot check Gemini API usage without a gcloud project ID.")