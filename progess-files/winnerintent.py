from athenaservicecall import athenaservicecall

def get_var_char_values(d):
    return [obj['VarCharValue'] for obj in d['Data']]


def winnerintent(DATABASE, TABLE, S3_OUTPUT, kwargs):
    # created query
    date = kwargs["date"]
    winner_query = "select winner from ipldataset.inputiplbucket where inputiplbucket.date='"+date+"';"
    print("winner_query:",winner_query)
    results = athenaservicecall(winner_query, DATABASE, S3_OUTPUT)

    for row in results['ResultSet']['Rows'][1:]:
        row_result = row["Data"][0]["VarCharValue"]
        if (kwargs["team_one"] == row_result):
            winner = kwargs["team_one"]
        elif(kwargs["team_two"] ==  row_result):
            winner = kwargs["team_two"]
        else:
            winner = "unknown"
    
        return winner
