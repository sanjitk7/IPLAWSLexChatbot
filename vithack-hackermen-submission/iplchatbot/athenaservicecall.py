import boto3
import time

# number of retries
RETRY_COUNT = 10


def athenaservicecall(query_string, Database, OutputLocation):
    # athena client
    client = boto3.client('athena')
    response = client.start_query_execution(
        QueryString=query_string,
        QueryExecutionContext={
            'Database': Database
        },
        ResultConfiguration={
            'OutputLocation': OutputLocation
        }
    )

    # get query execution id
    query_execution_id = response['QueryExecutionId']

    for i in range(1, 1 + RETRY_COUNT):

        # get query execution
        query_status = client.get_query_execution(
            QueryExecutionId=query_execution_id)
        print(query_status)
        query_execution_status = query_status['QueryExecution']['Status']['State']

        if query_execution_status == 'SUCCEEDED':
            print("STATUS:" + query_execution_status)
            break

        if query_execution_status == 'FAILED':
            raise Exception("STATUS:" + query_execution_status)

        else:
            print("STATUS:" + query_execution_status)
            time.sleep(i)
    else:
        client.stop_query_execution(QueryExecutionId=query_execution_id)
        raise Exception('TIME OVER')

    # get query results
    result = client.get_query_results(QueryExecutionId=query_execution_id)
    return result
