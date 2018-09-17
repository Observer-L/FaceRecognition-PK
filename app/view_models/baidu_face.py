class BaiduFaceModel:
    def __init__(self, result):
        self.face_num = result['face_num']
        self.face_list = result['face_list']
        self.faces = []
        for face in self.face_list:
            face_info = {}
            face_info['face_token'] = face['face_token']
            face_info['gender'] = face['gender']
            face_info['age'] = face['age']
            face_info['race'] = face['race']
            face_info['beauty'] = face['beauty']
            face_info['expression'] = face['expression']
            face_info['face_shape'] = face['face_shape']
            face_info['glasses'] = face['glasses']
            face_info['location'] = face['location']

            self.faces.append(face_info)




