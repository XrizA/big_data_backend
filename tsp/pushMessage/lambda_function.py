from alert_notification import AlertNotification
from alert_notification_config import RECEIVER_LINE_ID, CHANNEL_ACCESS_TOKEN

def lambda_handler(event, context):
    alert_notification = AlertNotification(event, RECEIVER_LINE_ID, CHANNEL_ACCESS_TOKEN)
    push_result = alert_notification.alert_notification()
    return push_result
