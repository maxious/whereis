import json
from whereis import maps, trains


def hello(event, context):

    people_latlons = maps.get_people_latlons()
    train_latlons = trains.get_filtered_latlons('IWL_1*|BWT_1*')
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
