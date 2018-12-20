#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  camera_pi.py
#  
#  
# 
import face_recognition
import cv2 
import time
import io
import threading


class Camera(object):

    def __init__(self):
        print("Iniciando Clase")
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True


    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    def load_people(self):
        print ("Cargando Personas de Interés")
        # Load a sample picture and learn how to recognize it.
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


    def initialize(self):
        print ("Iniciando threads")

        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        
        Camera.last_access = time.time()
        self.initialize()
        
        print ("Obteniendo Frame")

        return self.frame

    @classmethod
    def _thread(cls):
        print ("Thread Principal")

        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        # Grab a single frame of video
        video_capture = cv2.VideoCapture('http://192.168.0.30:8160')

        stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # store frame
                stream.seek(0)
                cls.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()




        
        ret, cls.frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(cls.frame, (0, 0), fx=0.25, fy=0.25)

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
                    #r = requests.post(API_ENDPOINT, data=json.dumps(data), headers=headers)

                    #idPersona = switch.get(name, "no reconocido")

                    print("Se ha identificado a "+name)
                    print("Id "+str(idPersona))

                    pastebin = r.text
                    print(pastebin)

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
            cv2.rectangle(cls.frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(cls.frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(cls.frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


        #with picamera.PiCamera() as camera:
            # camera setup
        #    camera.resolution = (320, 240)
        #    camera.hflip = True
        #    camera.vflip = True

            # let camera warm up
        #    camera.start_preview()
        #    time.sleep(2)

            #stream = io.BytesIO()
            #for foo in camera.capture_continuous(stream, 'jpeg',use_video_port=True):
                # store frame
            #    stream.seek(0)
            #    cls.frame = stream.read()

                # reset stream for next frame
            #    stream.seek(0)
            #    stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
            if time.time() - cls.last_access > 10:
                break
        cls.thread = None