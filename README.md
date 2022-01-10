#WebCam with python and opencv

##install dependencies
```commandline
pip install flask
pip install flask-apscheduler
pip install opencv-python
```

##how to run:
```commandline
flask run
```
if camera not works, change self.camera_number = 1 to 0 in class Camera

port: http://127.0.0.1:5000/

##api:
```
/ :live stream
/capture :screen shot
/video_list :list of saved video
/download :download a video (the video file name need to be given in request body)
```