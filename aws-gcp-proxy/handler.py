import json
import os
import requests
from datetime import datetime


def printJson(jsonObject, label):
    """Pretty print JSON document with indentation."""
    systime = str(datetime.now())
    print("************************ {} *********************".format(label))
    print("----------------------- {} -----------------------".format(systime))
    print(json.dumps(jsonObject, indent=4, sort_keys=True))
    print("------------------------------------------------------------------")


def process(event, context):
    """
    Act as a proxy for Google Vision image detection.

    Read the 'imageUri' parameter from the input request and call the Google
    Function fronted by the URL passed in the environment variable GFUNC_URL.
    """
    printJson(event, 'Incoming event object')
    body = {
        "imageAnalyzed": "",
        "message": "Nothing yet!",
        "report": "",
        "input": event
    }

    myReport = "Smooth sailing!"
    gfunc_url = os.environ['GFUNC_URL']
    myImageUri = 'https://goo.gl/Cb9xTN'
    try:
        myImageUri = event['queryStringParameters']['imageUri']
    except:
        myReport = \
         "No imageUri param passed. Using {} as imageUri".format(myImageUri)
        print(myReport)
    myParams = {'imageUri': myImageUri}
    r = requests.get(gfunc_url, params=myParams)
    body['message'] = r.text
    body['imageAnalyzed'] = myImageUri
    body['report'] = myReport
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code  if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
