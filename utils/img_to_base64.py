import base64


def img_to_base64(img_path):
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())
    return img