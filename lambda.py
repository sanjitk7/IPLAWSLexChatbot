import json
import boto3
import time


def lambda_handler(event, context):
    client = boto3.client('athena')

    # setup and perform query
    queryStart = client.start_query_execution(
        QueryString="SELECT * FROM ill_bucket_vithack limit 20;",
        QueryExecutionContext={
            'Database': 'ill-bucket-vithack'
        },
        ResultConfiguration={
            'OutputLocation': 's3://ipl-results/'
        }
    )
    # Observe results
    queryId = queryStart['QueryExecutionId']
    time.sleep(15)

    results = client.get_query_results(QueryExecutionId=queryId)
    for row in results['ResultSet']['Rows']:
        print(row)
