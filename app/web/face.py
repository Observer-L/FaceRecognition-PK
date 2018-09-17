from flask import render_template, flash, jsonify, request
from api import Azureface, Baiduface, FacePP
from app.view_models import BaiduFaceModel, AzureFaceModel
# img_trump = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Donald_Trump_official_portrait.jpg/800px-Donald_Trump_official_portrait.jpg"
from app.web import web


@web.route('/face', methods=["POST"])
def index():
    diff_face_api_results = {}
    bf = Baiduface()
    af = Azureface()

    try:
        img_url = request.form.get('img_url')
        af_data = AzureFaceModel(af.reconize_face(img_url=img_url)).faces
        diff_face_api_results['Azure'] = af_data

        bf_data = bf.reconize_face(img_url=img_url)
        if not bf_data['error_code']:
            bf_data = BaiduFaceModel(bf_data['result']).faces
            diff_face_api_results['BaiduAI'] = bf_data
        else:
            bf_data = None
            flash(str(bf_data['error_code']) + '：' + bf_data['error_msg'])

    except Exception as e:
        flash(e)
    print(diff_face_api_results)
    return jsonify(diff_face_api_results)
