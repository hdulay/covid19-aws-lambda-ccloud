import json

# AWS LAMBDA FUNCTION - Copy paste into lambda aws ui

def lambda_handler(event, context):
    result_list = []
    for body in event:
        result = {}
        result["body"] = body
        result["status_code"] = 200
        result_list.append(result)
    return result_list
