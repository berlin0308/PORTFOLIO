import cv2

def capture_video(t, fps, file_name):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, fps)
    # cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
    # cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
    # cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    # cap.set(cv2.CAP_PROP_FOCUS, focus)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(file_name, fourcc, fps, (1280, 720))

    duration = t * fps
    # frame_count = 0
    # while frame_count < duration:
    #     print(frame_count)
    #     ret, frame = cap.read()
    #     if ret:
    #         # cv2.imshow('show', frame)
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         out.write(frame)
    #         frame_count += 1
    #     else:
    #         break
        
    
    images = []
    for i in range(duration):
        ret, frame = cap.read()
        images.append(frame)
        # print(i)
   
    for image in images:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        out.write(image_rgb)

    cap.release()
    out.release()
    # cv2.destroyAllWindows()


capture_video(t=1,fps=30,file_name="C:/Users/BERLIN CHEN/Desktop/CALF/DATA_PREP/captured_video_2.mp4")