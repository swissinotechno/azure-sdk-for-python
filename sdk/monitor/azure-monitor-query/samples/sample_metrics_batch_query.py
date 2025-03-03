# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""
FILE: sample_metrics_batch_query.py
DESCRIPTION:
    This sample demonstrates authenticating the MetricsBatchQueryClient and retrieving the "Ingress"
    metric along with the "Average" aggregation type for multiple resources.
    The query will execute over a timespan of 2 hours with a granularity of 5 minutes.
USAGE:
    python sample_metrics_batch_query.py
    1) AZURE_METRICS_ENDPOINT - The regional metrics endpoint to use (i.e. https://westus3.metrics.monitor.azure.com)

    This example uses DefaultAzureCredential, which requests a token from Azure Active Directory.
    For more information on DefaultAzureCredential, see https://learn.microsoft.com/python/api/overview/azure/identity-readme?view=azure-python#defaultazurecredential.

    In this example, storage account resource URIs are queried for metrics.
"""

# [START send_metrics_batch_query]
from datetime import timedelta
import os

from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsBatchQueryClient, MetricAggregationType


endpoint = os.environ["AZURE_METRICS_ENDPOINT"]

credential = DefaultAzureCredential()
client = MetricsBatchQueryClient(endpoint, credential)

resource_uris = [
    '/subscriptions/<id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<account-1>',
    '/subscriptions/<id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<account-2>'
]

try:
    response = client.query_batch(
        resource_uris,
        metric_names=["Ingress"],
        metric_namespace="Microsoft.Storage/storageAccounts",
        timespan=timedelta(hours=2),
        granularity=timedelta(minutes=5),
        aggregations=[MetricAggregationType.AVERAGE],
    )

    for metrics_query_result in response:
        for metric in metrics_query_result.metrics:
            print(metric.name + " -- " + metric.display_description)
            for time_series_element in metric.timeseries:
                for metric_value in time_series_element.data:
                    print("The ingress at {} is {}".format(metric_value.timestamp, metric_value.average))
except HttpResponseError as err:
    print("something fatal happened")
    print(err)
# [END send_metrics_batch_query]
