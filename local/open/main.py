import boto3
import time
import pafy
import cv2
from API.capture import Capture
from config import (
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME, STEP_FUNCTION_ACTIVATE_FREQENCY,
    SITE, SOURCE_URL, STEP_FUNCTION_ARN
)
import json
import threading
import keyboard

client = boto3.client(
    'stepfunctions',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION_NAME)

def stream():
    print('Streaming.........')
    video_id = pafy.new(SOURCE_URL)
    stream_url = video_id.getbest(preftype='mp4').url
    video_capture = cv2.VideoCapture(stream_url)
    global frame
    while True:
        try:
            if video_capture.isOpened():
                if ret == False:
                    continue
                
                data_model = Capture().frame(frame, SITE)
                
                client.start_execution(
                    stateMachineArn=STEP_FUNCTION_ARN,
                    input=json.dumps(data_model)
                )
            else:
                print("frame is not ready")
                cv2.waitKey(1000)
                continue
                
            cv2.waitKey(10)
            if ret == False:
                video_capture = cv2.VideoCapture(stream_url)
        except:
            print('Source video is unavailable! reconnecting ....')
            cv2.destroyAllWindows()
            break
            
    time.sleep(1)
        

streaming_thread = threading.Thread(target = stream, daemon = True)
streaming_thread.start()

def main():
    while True:
        if frame is not None:
            data_model = Capture().frame(frame, SITE)
            
            if keyboard.is_pressed("q"):
                print("Register set to True")
                client.start_execution(
                    stateMachineArn=STEP_FUNCTION_ARN,
                    input=json.dumps(data_model)
                )
            else:
                print("Register set to False")
                
            time.sleep(STEP_FUNCTION_ACTIVATE_FREQENCY)
        else:
            print("No frame")
            
            time.sleep(1)
            
    print("system set to False")
    time.sleep(1)

if __name__ == '__main__':
    main()
