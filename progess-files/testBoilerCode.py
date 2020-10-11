import boto3
import time

# number of retries
RETRY_COUNT = 10

Mumbai Indians
Mumbai Indians
# def athenaservicecall(query_string="select winner from ipldataset.inputiplbucket;", Database="ipldataset", OutputLocation="s3://outputiplbucket/"):
def athenaservicecall(event,context):
    # athena client
    client = boto3.client('athena')
    response = client.start_query_execution(
        QueryString=event["query_string"],
        QueryExecutionContext={
            'Database': event["Database"]
        },
        ResultConfiguration={
            'OutputLocation': event["OutputLocation"]
        }
    )

    # get query execution id
    query_execution_id = response['QueryExecutionId']
    print("athenaservicecall queryexecution id:", query_execution_id)

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
    print(result)
    return result
