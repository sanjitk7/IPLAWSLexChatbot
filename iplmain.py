import time
import boto3
from winnerintent import winnerintent

# athena constant
DATABASE = 'ipldataset'
TABLE = 'inputiplbucket'

# S3 constant
S3_OUTPUT = 's3://outputiplbucket/'
S3_BUCKET = 'outputiplbucket'

# query constant
COLUMN = 'team1'


def lambda_handler(event, context):

    winnerintent(DATABASE, TABLE, S3_OUTPUT)
