import cv2
import datetime

""" 
2023.3.1
10fps是最高的了 用ffmpeg檢查沒問題 時間也是正確的
"""

def capture_video(t, fps, file_id):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, fps)
    # cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
    # cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
    # cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    # cap.set(cv2.CAP_PROP_FOCUS, focus)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    complete_file_name = "/home/pi/CALF/DATA_PREP/Video_save_test/{}.mp4".format(file_id)
    out = cv2.VideoWriter(complete_file_name, fourcc, fps, (1280, 720))

    duration = t * fps
    for i in range(duration):
        ret, frame = cap.read()
        if ret:
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(image_rgb)
        
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Video saved: {}".format(complete_file_name))


update_time = datetime.datetime.now()
while True:
    now = datetime.datetime.now()
    if now-update_time > datetime.timedelta(seconds=10):
        update_time = now
        capture_video(t=4,fps=10,file_id=now.strftime("%Y%m%d-%H-%M-%S"))