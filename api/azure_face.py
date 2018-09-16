import json
import os
import urllib.request
from urllib import parse
import http.client
from config.config import azure_config
from utils import json_byte_to_dict, img_to_base64, img_to_binary


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
            conn.close()
        except Exception as e:
            return "Error: " + e

        return face_info_dict

    def get_preson_info(self, face_info_dict):
        """
        返回基本的识别信息
        :param face_info_dict:
        :return: info_dict
        """
        info_dict = {}
        # 待细分
        face = face_info_dict[0]
        faceAttributes = face['faceAttributes']
        info_dict['faceRectangle'] = face['faceRectangle']
        info_dict['gender'] = faceAttributes['gender']
        info_dict['age'] = faceAttributes['age']
        info_dict['facialHair'] = faceAttributes['facialHair']
        info_dict['glasses'] = faceAttributes['glasses']
        return info_dict


if __name__ == '__main__':
    af = Azureface()
    img_path = os.path.abspath(os.path.dirname(os.getcwd())) + r'\images\einstein.jpg'    # 爱因斯坦吐舌头
    img_url = "https://www.pcmarket.com.hk/wp-content/uploads/2018/03/usa-election_trump1-770x439_c.jpg"    # 特朗普怒竖指
    info_dict = af.reconize_face(img_url=img_url)
    print(af.get_preson_info(info_dict))
    # af.reconize_face(img_path=img_path)