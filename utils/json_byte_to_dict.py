import json


def json_byte_to_dict(json_byte_file):
    """
    将byte格式的json文件转换成字典格式的文件
    :param json_byte_file:
    :return: dict
    """
    str_json = json_byte_file.decode()
    str_dict = json.loads(str_json)
    return str_dict