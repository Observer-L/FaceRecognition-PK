class FacePPFaceModel:
    def __init__(self, result):
        faces = result['faces']
        self.face_num = len(faces)
        self.faces = []
        for face in faces:
            face_info = {}
            attrs = face['attributes']
            for attr in attrs:
                face_info[attr] = attrs[attr]

            face_info['face_rectangle'] = face['face_rectangle']
            face_info['face_token'] = face['face_token']

            self.faces.append(face_info)




