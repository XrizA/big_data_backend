from object_detection import ObjectDetection
from person_detection_config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    REGION_NAME,
    BUCKET_NAME
)

def lambda_handler(event, context):
    object_detection = ObjectDetection(
        event,
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY,
        REGION_NAME
    )
    object_detection.store_image(BUCKET_NAME)
    response = object_detection.object_detect()
    object_detection.person_dectect_parse(response, BUCKET_NAME)
    return { "statusCode": 200, "body": object_detection.get_data_model() }
