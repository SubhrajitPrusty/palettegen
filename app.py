import os
from flask import Flask, render_template, Response
from camera import VideoCamera
from gevent.pywsgi import WSGIServer

app = Flask(__name__, static_url_path="/static")

@app.route("/", methods=["GET"])
def index():
	return render_template("index.html")

def gen(camera):
	while True:
		frame = camera.getFrame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/video_feed")
def video_feed():
	return Response(gen(VideoCamera()), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	http_server = WSGIServer(('', port), app)
	http_server.serve_forever()
