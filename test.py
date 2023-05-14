from flask import Flask, render_template, Response
from picamera import PiCamera
import time

app = Flask(__name__)

def generate_frames():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30
    time.sleep(2)  # Temps d'attente pour permettre à la caméra de se stabiliser

    while True:
        frame = camera.capture_bytes(format='jpeg')

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
