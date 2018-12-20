import time
import cv2
import os 
import paramiko 


#Identificación de la camara
camera_id = 1

camera = cv2.VideoCapture(0)

#Conexión
host = "areatecnica.cl"
port = 22222
user = "root"
password = "NintendO64"
server_path = '/var/www/html/images/'
local_path = 'home/image.jpg'


#Tamaño de la captura
height=480*2
width=640*2


def upload():
	transport = paramiko.Transport((host, port))
	transport.connect(username=user, password = password)
	sftp = paramiko.SFTPClient.from_transport(transport)
	sftp.put('image.jpg', server_path+str(camera_id)+'.jpg')
	
	sftp.close()
	transport.close()
	return 'Imagen subida exitosamente'

try:
	os.remove("image.jpg")
	print ("Limpiando datos previos")
except Exception:
	print ("No se han encontrados datos previos")

while True:
	
	ret, frame = camera.read()
	cv2.imwrite('image.jpg', frame)

	print(upload()+" "+time.strftime("%Y-%m-%d %H:%M:%S"))

	time.sleep(2)

camera.release();
