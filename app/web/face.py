from flask import render_template, flash, jsonify, request
from api import Azureface, Baiduface, FacePP
from app.view_models.baidu_face import BaiduFaceModel

from . import web
# img_trump = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Donald_Trump_official_portrait.jpg/800px-Donald_Trump_official_portrait.jpg"


@web.route('/face', methods=["POST"])
def index():
    bf = Baiduface()
    try:
        img_url = request.form.get('img_url')
        print(img_url)
        data = bf.reconize_face(img_url=img_url)
        if not data['error_code']:
            data = BaiduFaceModel(data['result'])
            # return render_template('index.html', data=data.faces, img_url=img_trump)
            return jsonify(data.faces)
        else:
            flash(str(data['error_code']) + '：' + data['error_msg'])
    except Exception as e:
        flash(e)
    return jsonify(e)
    # return render_template('index.html')
