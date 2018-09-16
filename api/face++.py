import os
import urllib.request
from urllib import parse

from config.config import facePP_config
from utils import json_byte_to_dict, img_to_base64


class FacePP:
    def __init__(self):
        self.api_key = facePP_config['APIKEY']
        self.api_secret = facePP_config['APISECRET']
        self.url = facePP_config['REQUEST_URL_V3']

    def reconize_face(self, img_url=None, img_path=None, return_landmark=0):
        """
        返回基本的识别信息
        :param img_url:
        :param img_path:
        :param return_landmark:
        :return:
        """
        params = {
            'api_key': self.api_key,
            'api_secret': self.api_secret,
            'return_landmark': return_landmark,
            'return_attributes': 'gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity'   # 请不要用空格分隔
        }

        if img_path:
            params['image_base64'] = img_to_base64(img_path)
        elif img_url:
            params['image_url'] = img_url

        params = parse.urlencode(params).encode('utf-8')
        response = urllib.request.urlopen(self.url, params)
        content = response.read()
        face_info_dict = json_byte_to_dict(content)
        return face_info_dict

    def get_preson_info(self, face_info_dict):
        """
        返回基本的识别信息
        :param face_info_dict:
        :return: info_dict
        """
        info_dict = {}
        faces = face_info_dict['faces']
        face_one = faces[0]  # 先处理1个
        attrs = face_one['attributes']
        info_dict['face_rectangle'] = face_one['face_rectangle']
        info_dict['emotion'] = attrs['emotion']
        info_dict['gender'] = attrs['gender']
        info_dict['age'] = attrs['age']
        info_dict['eyestatus'] = attrs['eyestatus']  # 左右眼睛状态（合闭、眼镜、是否为黑框眼镜 @_@ ）
        info_dict['headpose'] = attrs['headpose']
        info_dict['ethnicity'] = attrs['ethnicity']  # 种族
        return info_dict


if __name__ == '__main__':
    img_path = os.path.abspath(os.path.dirname(os.getcwd())) + r'\images\einstein.jpg'  # 爱因斯坦吐舌头
    img_url = 'https://www.pcmarket.com.hk/wp-content/uploads/2018/03/usa-election_trump1-770x439_c.jpg'  # 特朗普怒竖指
    # 低像素，多人照片
    img_url_more = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1537109119958&di=184ceb74e77b081542163c6cea750822&imgtype=0&src=http%3A%2F%2Fn.sinaimg.cn%2Fsinacn11%2F709%2Fw400h309%2F20180319%2Ff469-fyskeuc0782277.jpg'
    fpp = FacePP()
    # fpp.get_info(img_path=img_path)
    # print(fpp.get_info(img_url=img_url))
    # print(fpp.reconize_face(img_url=img_url_more))
    face_info_dict = fpp.reconize_face(img_url=img_url_more)
    print(fpp.get_preson_info(face_info_dict))