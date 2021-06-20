from linebot import LineBotApi
from linebot.models import PostbackAction
from linebot.models.send_messages import TextSendMessage
from linebot.models.template import CarouselColumn, TemplateSendMessage, CarouselTemplate
import time
from datetime import datetime
from pytz import timezone

class AlertNotification:
    def __init__(self, data_model, receiver_line_id, channel_access_token):
        self.__data_model = data_model
        self.__receiver_line_id = receiver_line_id
        self.__channel_access_token = channel_access_token

    def alert_notification(self):
        '''
        is_danger = self.__data_model['alertNotify']['isDanger']
        if is_danger == False:
            return
        '''
        person_threshold = self.__data_model['personDetection']['threshold']
        person_count = self.__data_model['personDetection']['personCount']
        if person_count < person_threshold:
            return
        
        line_bot_api = LineBotApi(self.__channel_access_token)

        origin_image_url = self.__data_model['imageUrl']
        site = self.__data_model['site']
        
        fmt = '%Y-%m-%d %H:%M:%S'
        taipei = timezone('Asia/Taipei')
        
        event_timestamp = self.__data_model['timestamp']
        notify_timestamp = time.time()
        event_datetime = datetime.fromtimestamp(int(event_timestamp))
        event_datetime = event_datetime.astimezone(taipei).strftime(fmt)
        notify_datetime = datetime.fromtimestamp(int(notify_timestamp))
        notify_datetime = notify_datetime.astimezone(taipei).strftime(fmt)
        
        '''
        danger_person_image_url_list = self.__data_model['alertNotify']['dangerPersonImageUrlList']
        cross_count = len(danger_person_image_url_list)
        
        carousel_columns = []
        
        origin_frame_carousel_colum = CarouselColumn(
            thumbnail_image_url = origin_image_url,
            title = '現場圖片',
            text = '時間：%s' % (event_datetime),
            actions = [
                PostbackAction(
                    label = ' ',
                    data = 'doNothing'
                )
            ]
        )
        
        carousel_columns.append(origin_frame_carousel_colum)
        
        carousel_colum = None
        
        for danger_person_image_url in danger_person_image_url_list:
            carousel_colum = CarouselColumn(
                thumbnail_image_url = danger_person_image_url,
                title = '逾界',
                text = '時間：%s' % (event_datetime),
                actions = [
                    PostbackAction(
                        label = ' ',
                        data = 'doNothing'
                    )  
                ]
            )
            carousel_columns.append(carousel_colum)
            
        
            
        carouselTemplate = TemplateSendMessage(
            alt_text = '收到通報訊息',
            template = CarouselTemplate(
                columns = carousel_columns
            )
        )
        '''
        
        text = '地點：%s\n事件時間：%s\n通報時間：%s\n\n總人數：%s\n閥值為：%s\n總人數已經超過所設定的閥值人數' % (site, event_datetime, notify_datetime, person_count, person_threshold)
        detect_result_template_message = TextSendMessage(text=text)
            
        # line_bot_api.push_message(self.__receiver_line_id, [carouselTemplate, detect_result_template_message])
        line_bot_api.push_message(self.__receiver_line_id, detect_result_template_message)
        
        return {'statusCode': 200, 'body': 'Success'}
