import os
import urllib.request
from urllib import parse

from utils import json_byte_to_dict, img_to_base64
import sys
sys.path.append("..")
from config import facePP_config


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
            'return_attributes': 'gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,skinstatus'   # 请不要用空格分隔
        }

        if img_path:
            params['image_base64'] = img_to_base64(img_path)
        elif img_url:
            params['image_url'] = img_url

        params = parse.urlencode(params).encode('utf-8')
        try:
            response = urllib.request.urlopen(self.url, params)
        except Exception as e:
            return {'error': str(e)}
        content = response.read()
        face_info_dict = json_byte_to_dict(content)
        return face_info_dict



if __name__ == '__main__':
    img_path = os.path.abspath(os.path.dirname(os.getcwd())) + r'\images\einstein.jpg'  # 爱因斯坦吐舌头
    img_url = 'https://www.pcmarket.com.hk/wp-content/uploads/2018/03/usa-election_trump1-770x439_c.jpg'  # 特朗普怒竖指
    # 低像素，多人照片
    img_url_more = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1537109119958&di=184ceb74e77b081542163c6cea750822&imgtype=0&src=http%3A%2F%2Fn.sinaimg.cn%2Fsinacn11%2F709%2Fw400h309%2F20180319%2Ff469-fyskeuc0782277.jpg'
    fpp = FacePP()
    face_info_dict = fpp.reconize_face(img_url=img_url_more)
    print(face_info_dict)