import cv2
import face_recognition
import requests
from base_camera import BaseCamera


class Camera(BaseCamera):
    
    ENDPOINT = "http://www.areatecnica.cl:28080/plaza_segura_restful-1.0/webresources/com.areatecnica.plaza_segura_restful.entities.alerta/"
    video_source = 'http://192.168.43.129:8160'
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    
# Load a sample picture and learn how to recognize it.
    


    @staticmethod
    def load_faces():
        print ("Cargando personas")
        

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('No se puede cargar el streaming')

        process_this_frame = True

        obama_image = face_recognition.load_image_file("ian.jpg")
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

            # Load a second sample picture and learn how to recognize it.
        biden_image = face_recognition.load_image_file("romina.jpg")
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

            # Create arrays of known face encodings and their names
        known_face_encodings = [
            obama_face_encoding,
            biden_face_encoding
        ]

        known_face_names = [
            "Ian Concha",
            "Romina Torres"
        ]

        switch = {
            "Ian Concha": 1,
            "Romina Torres":2
        }

        while True:
            # read current frame
            _, img = camera.read()

            small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Desconocido"

                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]

                        # your source code here
                        #data = {'alertaIdTipo': 3, 'alertaIdCamara': 2, 'alertaDescripcion':name}
                        #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                        #r = requests.post(ENDPOINT, data=json.dumps(data), headers=headers)

                        idPersona = switch.get(name, "no reconocido")

                        print("Se ha identificado a: "+name)
                        print("Id:  "+str(idPersona))



                        #pastebin = r.text
                        #print(pastebin)

                    face_names.append(name)

            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)



            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()