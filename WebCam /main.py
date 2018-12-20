from flask import Flask, request, render_template, Response
from camera1 import Camera

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    #camera.load_people();
    """Video streaming generator function."""
    while True:
        #frame = camera.frames()
        #print ("valor: "+str(frame))
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + camera.frames() + b'\r\n')
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port =5000, debug=True, threaded=True)