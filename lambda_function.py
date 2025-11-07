import os
import json
import urllib3

http = urllib3.PoolManager()

def lambda_handler(event, context):
    print("FunctionHandler received: ", json.dumps(event))

    try:
        body = event.get("body")
        if body:
            data = json.loads(body)
        else:
            data = event 

        issue_url = data.get("issue", {}).get("html_url")

        if not issue_url:
            print("No issue found")
            return {"statusCode": 400, "body": "No issue found"}

        slack_url = os.environ.get("SLACK_URL")

        if not slack_url:
            print("Missing Slack URL")
            return {"statusCode": 500, "body": "Missing Slack URL"}

        message = {"text": f"Issue Created: {issue_url}"}

        encoded_msg = json.dumps(message).encode("utf-8")
        response = http.request("POST", slack_url, body=encoded_msg, headers={"Content-Type": "application/json"})

        print("Posted to Slack, response: ", response.status)
        return {"statusCode": 200, "body": "Success"}
    
    except Exception as e:
        print("Error: ", str(e))
        return {"statusCode": 500, "body": str(e)}
