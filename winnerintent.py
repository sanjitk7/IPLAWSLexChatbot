from athenaservicecall import athenaservicecall


def winnerintent(DATABASE, TABLE, S3_OUTPUT):
    # created query
    query_string = "SELECT * FROM `%s`.`%s`;" % (DATABASE, TABLE)
    getPreviewQuery = "SELECT * FROM ipldataset.inputiplbucket limit 10;"

    results = athenaservicecall(query_string, DATABASE, S3_OUTPUT)

    print("athenaQuery Result:")
    for row in results['ResultSet']['Rows']:
        print(row)
