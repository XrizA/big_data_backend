import alert_notification_config
import thirdPartyServiceProviderConfig
import requests

client = boto3.client('lambda',aws_access_key_id = config.aws_access_key_id,aws_secret_access_key = config.aws_secret_access_key,region_name = config.region_name)

def lambda_handler(event, context):
    response = requests.post(thirdPartyServiceProviderConfig.Line_TSP_Url, data = json.dumps({
    "receiverLineIdList":receiverLineIdList,
    "messages":messages,
    "Content-Type":"application/json"
    }), headers={
    "x-api-key" : thirdPartyServiceProviderConfig.Line_Api_Key
    })    
    return "suceess"
