from athenaservicecall import athenaservicecall


def winnerintent(DATABASE, TABLE, S3_OUTPUT, kwargs):
    # created query
    # query_string = "SELECT * FROM `%s`.`%s`;" % (DATABASE, TABLE)
    # getPreviewQuery = "SELECT * FROM ipldataset.inputiplbucket limit 10;"
    date = kwargs["date"]
    winner_query = "select winner from ipldataset.inputiplbucket where inputiplbucket.date=03/04/19;"
    print("winner_query:",winner_query)
    results = athenaservicecall(winner_query, DATABASE, S3_OUTPUT)

    print("athenaQuery Result:", results)

    for row in results['ResultSet']['Rows']:
        print(row)

    if (kwargs["team_one"] in results['ResultSet']['Rows']):
        winner = kwargs["team_one"]
    elif(kwargs["team_two"] in results['ResultSet']['Rows']):
        winner = kwargs["team_two"]
    else:
        winner = "unknown"

    return winner
