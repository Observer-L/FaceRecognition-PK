import json
import os
import urllib.request
from urllib import parse
import http.client
# from config2.config2 import azure_config
from utils import json_byte_to_dict, img_to_base64, img_to_binary
import sys
sys.path.append("..")
import sys
sys.path.append("..")
from config import azure_config


class Azureface:
    def __init__(self):
        self.api_key = azure_config['APPKEY']
        self.url = azure_config['REQUEST_URL']

    def reconize_face(self, img_url=None, img_path=None, returnFaceId='true', returnFaceLandmarks='false'):
        """
        返回基本的识别信息
        :param returnFaceId:
        :param returnFaceLandmarks:
        :return: face_info_dict
        """
        params = urllib.parse.urlencode({
            'returnFaceId': returnFaceId,
            'returnFaceLandmarks': returnFaceLandmarks,
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses',  # TODO: 更多特征
        })
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        if img_path:
            body = img_to_binary(img_path) # FIXME
        elif img_url:
            body = json.dumps({"url": img_url})

        try:
            conn = http.client.HTTPSConnection('api.cognitive.azure.cn')
            conn.request("POST", self.url+'?%s' % params, body, headers=headers)
            response = conn.getresponse()
            content = response.read()
            face_info_dict = json_byte_to_dict(content)
            face_info_dict = {'error': face_info_dict['error']['message']} if not isinstance(face_info_dict, list) and face_info_dict['error'] else face_info_dict
            conn.close()
        except Exception as e:
            return "Error: " + str(e)

        return face_info_dict


if __name__ == '__main__':
    af = Azureface()
    img_path = os.path.abspath(os.path.dirname(os.getcwd())) + r'\images\einstein.jpg'    # 爱因斯坦吐舌头
    img_url = "https://www.pcmarket.com.hk/wp-content/uploads/2018/03/usa-election_trump1-770x439_c.jpg"    # 特朗普怒竖指
    info_dict = af.reconize_face(img_url=img_url)
    print(info_dict)