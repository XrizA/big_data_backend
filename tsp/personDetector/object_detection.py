import boto3
from base64 import b64decode, b64encode
from datetime import datetime
import cv2
import numpy
from pytz import timezone

class ObjectDetection:
    def __init__(self, data_model, aws_access_key_id, aws_secret_access_key, region_name):
        self.__data_model = data_model
        self.__region_name = region_name
        self.__s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.__rekognition_client = boto3.client(
            'rekognition',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.__taipei_timezone = timezone('Asia/Taipei')
        self.__fmt = '%Y-%m-%d %H:%M:%S'

    def store_image(self, bucket_name):
        client = self.__s3_client

        image = self.__data_model['image']
        image_binary = b64decode(image)

        frame_id = self.__data_model['frameId']

        file_name = '%s.jpeg' % (frame_id)
        
        timestamp = datetime.fromtimestamp(int(self.__data_model['timestamp']))
        timestamp = timestamp.astimezone(self.__taipei_timezone).strftime(self.__fmt)

        client.put_object(ACL='public-read', Body=image_binary, Bucket=bucket_name,
                          Key='%s/%s' % (timestamp, file_name), ContentEncoding='base64',
                          ContentType='image/jpeg')
        self.__data_model['imageUrl'] = 'https://%s.s3-%s.amazonaws.com/%s/%s' \
            % (bucket_name, self.__region_name, timestamp, file_name)

    def object_detect(self):
        client = self.__rekognition_client
        max_labels = 1000
        min_confidence = 0

        image = self.__data_model['image']
        image_binary = b64decode(image)

        response = client.detect_labels(
            Image={'Bytes': image_binary},
            MaxLabels=max_labels,
            MinConfidence=min_confidence)
        return response

    def person_dectect_parse(self, detect_labels, bucket_name):
        client = self.__s3_client
        image = self.__data_model['image']
        image_binary = b64decode(image)
        numpy_array = numpy.frombuffer(image_binary, numpy.uint8)
        original_image = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)
        size = original_image.shape
        height, width = size[0], size[1]
        person_list = []
        serial_number = 1

        for label in detect_labels['Labels']:
            if label['Name'] == 'Person':
                for instance in label['Instances']:
                    bounding_box = instance['BoundingBox']
                    upper_left_point_x = int(bounding_box['Left'] * width)
                    upper_left_point_y = int(bounding_box['Top'] * height)
                    lower_right_point_x = int(
                        (bounding_box['Left'] + bounding_box['Width']) * width)
                    lower_right_point_y = int(
                        (bounding_box['Top'] + bounding_box['Height']) * height)
                    crop_image = original_image[
                        upper_left_point_y: lower_right_point_y,
                        upper_left_point_x: lower_right_point_x
                    ]
                    crop_image = b64encode(cv2.imencode(
                        '.jpg', crop_image)[1]).decode()
                    cut_image_binary = b64decode(crop_image)

                    file_name = '%s.jpeg' % (serial_number)

                    timestamp = datetime.fromtimestamp(int(self.__data_model['timestamp']))
                    timestamp = timestamp.astimezone(self.__taipei_timezone).strftime(self.__fmt)

                    x = bounding_box['Left'] + bounding_box['Width'] / 2
                    y = bounding_box['Top'] + bounding_box['Height'] / 2

                    client.put_object(ACL='public-read', Body=cut_image_binary, Bucket=bucket_name,
                          Key='%s/%s' % (timestamp, file_name), ContentEncoding='base64',
                          ContentType='image/jpeg')

                    person_image_url = 'https://%s.s3-%s.amazonaws.com/%s/%s' \
                        % (bucket_name, self.__region_name, timestamp, file_name)                    

                    person_list.append({
                        'boundingBox': instance['BoundingBox'],
                        'coordination': { 'X': x, 'Y': y },
                        'personImageUrl': person_image_url
                    })

                    serial_number += 1
                self.__data_model['personDetection'] = {
                    'personCount': len(label['Instances']),
                    'personList': person_list
                }
                break
    def get_data_model(self):
        return self.__data_model
