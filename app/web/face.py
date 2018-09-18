from flask import flash, jsonify, request
from api import Azureface, Baiduface, FacePP
from app.view_models import BaiduFaceModel, AzureFaceModel, FacePPFaceModel
from app.web import web


@web.route('/face', methods=["POST"])
def index():
    diff_face_api_results = {}
    bf = Baiduface()
    af = Azureface()
    ff = FacePP()

    try:
        img_url = request.form.get('img_url')

        af_data = af.reconize_face(img_url=img_url)
        af_data = af_data if isinstance(af_data, dict) and 'error' in af_data else AzureFaceModel(af_data).faces

        bf_data = bf.reconize_face(img_url=img_url)
        bf_data = bf_data if 'error' in bf_data else BaiduFaceModel(bf_data).faces

        ff_data = ff.reconize_face(img_url=img_url)
        ff_data = ff_data if 'error' in ff_data else FacePPFaceModel(ff_data).faces

        diff_face_api_results['Azure'] = af_data
        diff_face_api_results['BaiduAI'] = bf_data
        diff_face_api_results['Face++'] = ff_data
    except Exception as e:
        print(e)

    return jsonify(diff_face_api_results)
