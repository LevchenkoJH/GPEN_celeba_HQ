import cv2
import os
from datetime import datetime

def video_to_frames(path):
    videoCapture = cv2.VideoCapture()
    videoCapture.open(path)
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    print("fps=", int(fps), "frames=", int(frames))

    dir_number = -1;
    dir_name = ""
    for i in range(int(frames)):
        ret, frame = videoCapture.read()
        file_name = str("%d.png" % (i))
        print(file_name.zfill(9), "/%d" % frames)

        ###################
        frame = cv2.resize(frame, (int(frame.shape[1] / 4), int(frame.shape[0] / 4)))
        ###################

        ###################
        if i >= (dir_number + 1) * 40:
            dir_number += 1
            dir_name = str(dir_number).zfill(3)
            os.mkdir("/home/jasmine/Framing/frames/" + dir_name)
        cv2.imwrite("/home/jasmine/Framing/frames/" + dir_name + "/" + file_name.zfill(9), frame)
        ###################



        ###################
        # cv2.imwrite("/home/jasmine/Framing/frames2/" + file_name.zfill(9), frame)
        ###################


if __name__ == '__main__':
    t1 = datetime.now()
    video_to_frames("videos/2.mp4")
    t2 = datetime.now()
    print("Time cost = ", (t2 - t1))