import cv2
import datetime
import os

def capture_video(t, fps, file_id):
    
    print("Start capturing... ",end="")
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, fps)
    # cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
    # cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
    # cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    # cap.set(cv2.CAP_PROP_FOCUS, focus)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    complete_file_name = "c:/Users/BERLIN CHEN/Desktop/CALF/DATA_PREP/video_mp4_save/{}.mp4".format(file_id)
    out = cv2.VideoWriter(complete_file_name, fourcc, fps, (1280, 720))

    duration = t * fps
    os.makedirs("c:/Users/BERLIN CHEN/Desktop/CALF/DATA_PREP/video_jpgs_save/{}".format(file_id), mode=0o777)
    for i in range(duration):
        ret, frame = cap.read()
        if ret:
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(image_rgb)
            complete_file_name_pngs = f"c:/Users/BERLIN CHEN/Desktop/CALF/DATA_PREP/video_jpgs_save/{file_id}/image_{i:05d}.jpg"
            cv2.imwrite(complete_file_name_pngs, image_rgb)
            print(str(i)+" ",end="")
        
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("\nVideo saved: C:/Users/BERLIN CHEN/Desktop/CALF/DATA_PREP/video_jpgs_save/{}/...".format(file_id))
    


update_time = datetime.datetime.now()
while True:
    now = datetime.datetime.now()
    if now-update_time > datetime.timedelta(seconds=10):
        update_time = now
        capture_video(t=4,fps=10,file_id=now.strftime("%Y%m%d-%H-%M-%S"))