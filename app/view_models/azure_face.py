class AzureFaceModel:
    def __init__(self, result):
        self.face_num = len(result)
        self.faces = []
        for face in result:
            face_info = {}
            face_info['faceId'] = face['faceId']
            face_info['faceRectangle'] = face['faceRectangle']
            face_attrs = face['faceAttributes']
            for attr in face_attrs:
                face_info[attr] = face_attrs[attr]

            self.faces.append(face_info)




