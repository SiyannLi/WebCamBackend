```commandline
pip install flask
pip install flask-apscheduler
pip install opencv-python
```

run:
```commandline
flask run
```

port: http://127.0.0.1:5000/

api:

```
/ :live stream
/capture :screen shot
/video_list :list of saved video
/download :download a video (the video file name need to be given in request body)
```