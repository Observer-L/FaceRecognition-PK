import base64
import urllib.request
from urllib import parse

import os

from utils import json_byte_to_dict
from config.config import baidu_config


class Baiduface:
    """
    向API服务地址使用POST发送请求，必须在URL中带上参数access_token，可通过后台的API Key和Secret Key生成
    client_id 为官网获取的AK， client_secret 为官网获取的SK
    :return:
    """
    def __init__(self):
        self.client_id = baidu_config['APIKEY']
        self.client_secret = baidu_config['SECRETKEY']
        self.host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'

        self.access_token = self.get_access_token(self.client_id, self.client_secret)

    def get_access_token(self, client_id=None, client_secret=None):
        """
        动态获取获取token
        :param client_id:
        :param client_secret:
        :return: access_token
        """
        host = self.host.format(client_id=client_id, client_secret=client_secret)
        request = urllib.request.Request(host)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        response = urllib.request.urlopen(request)
        content = response.read()
        token_dict = json_byte_to_dict(content)
        access_token = token_dict.get('access_token')
        return access_token

    def reconize_face(self, img_path=None, img_url=None, face_type='LIVE', quality_control='NORMAL', liveness_control='NONE'):
        """
        人脸检测
        :param img_path: 图片路径
        :param img_url: 图片URL
        :param face_type: 人脸的类型（LIVE、IDCARD、WATERMARK、CERT）
        :param quality_control: 图片质量控制（NONE、LOW、NORMAL、HIGH）
        :param liveness_control: 活体检测控制（NONE、LOW、NORMAL、HIGH）
        :return: face_info_dict
        """
        """
        图片类型
        BASE64: 图片的base64值，base64编码后的图片数据，编码后的图片大小不超过2M；
        URL: 图片的
        URL地址(可能由于网络等原因导致下载图片时间过长)；
        FACE_TOKEN: 人脸图片的唯一标识，调用人脸检测接口时，会为每个人脸图片赋予一个唯一的FACE_TOKEN，同一张图片多次检测得到的FACE_TOKEN是同一个。
        """
        # if img_path:
        if img_path:
            f = open(img_path, 'rb')
            img = base64.b64encode(f.read())
        img_type = 'URL' if img_url else 'BASE64'

        params = {
            "face_field": "age,beauty,expression,face_shape,gender,glasses,landmark,race,quality",  # 请不要用空格分隔
            "image": img,
            "image_type": img_type,
            "max_face_num": 5,
            "quality_control": quality_control,
            "liveness_control": liveness_control,
            "face_type": face_type
        }

        params = parse.urlencode(params).encode(encoding='UTF-8')
        access_token = self.access_token
        request_url = baidu_config['REQUEST_URL_V3'] + "?access_token=" + access_token

        request = urllib.request.Request(request_url, data=params)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib.request.urlopen(request)
        content = response.read()
        face_info_dict = json_byte_to_dict(content)
        return(face_info_dict)

    def get_preson_info(self, face_info_dict):
        """
        返回基本的识别信息
        :param face_info_dict:
        :return: info_dict
        """
        info_dict = {}
        result = face_info_dict['result']
        face_list = result['face_list'][0]  # 先处理1个
        info_dict['face_num'] = result['face_num']  # 脸数， 可通过max_face_num设定
        info_dict['location'] = face_list['location']   # 脸部定位
        info_dict['age'] = face_list['age']
        info_dict['beauty'] = face_list['beauty']   # 颜值
        info_dict['gender'] = face_list['gender']['type']
        info_dict['glasses'] = face_list['glasses']['type']
        info_dict['race'] = face_list['race']['type']
        info_dict['face_shape'] = face_list['face_shape']['type']
        return info_dict



if __name__ == '__main__':
    bf = Baiduface()
    # img_path = os.path.abspath(os.path.dirname(os.getcwd())) + r'\images\trump.jpg'    # 特朗普怒竖指
    img_path = os.path.abspath(os.path.dirname(os.getcwd())) + r'\images\einstein.jpg'    # 爱因斯坦吐舌头
    info_dict = bf.reconize_face(img_path=img_path)
    print(bf.get_preson_info(info_dict))

