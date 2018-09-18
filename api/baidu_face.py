import base64
import urllib.request
from urllib import parse

import os

from utils import json_byte_to_dict, img_to_base64
import sys
sys.path.append("..")
from config import baidu_config


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
        try:
            response = urllib.request.urlopen(request)
        except Exception as e:
            return {'error': str(e)}
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
        if not isinstance(self.access_token, str) and self.access_token['error']:
            return self.access_token

        params = {
            "face_field": "age,beauty,expression,face_shape,gender,glasses,landmark,race,quality",  # 请不要用空格分隔
            "max_face_num": 5,
            "quality_control": quality_control,
            "liveness_control": liveness_control,
            "face_type": face_type
        }

        if img_path:
            params['image'] = img_to_base64(img_path)
            params['image_type'] = 'BASE64'
        elif img_url:
            params['image'] = img_url
            params['image_type'] = 'URL'

        params = parse.urlencode(params).encode(encoding='UTF-8')
        request_url = baidu_config['REQUEST_URL_V3'] + "?access_token=" + self.access_token

        request = urllib.request.Request(request_url, data=params)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib.request.urlopen(request)
        content = response.read()
        face_info_dict = json_byte_to_dict(content)
        return(face_info_dict)





if __name__ == '__main__':
    bf = Baiduface()
    # img_path = os.path.abspath(os.path.dirname(os.getcwd())) + r'\images\trump.jpg'    # 特朗普怒竖指
    img_url_more = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1537109119958&di=184ceb74e77b081542163c6cea750822&imgtype=0&src=http%3A%2F%2Fn.sinaimg.cn%2Fsinacn11%2F709%2Fw400h309%2F20180319%2Ff469-fyskeuc0782277.jpg'
    info_dict = bf.reconize_face(img_url=img_url_more)
    print(info_dict)

