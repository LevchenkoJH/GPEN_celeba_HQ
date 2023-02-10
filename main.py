import cv2
import os
from datetime import datetime
import argparse
from tqdm import tqdm

def video_to_frames(input_dir, output_dir):
    dirs = sorted(os.listdir(input_dir))

    for video_path  in tqdm(dirs):
        video_path_tmp = os.path.join(input_dir, video_path)

        videoCapture = cv2.VideoCapture()
        videoCapture.open(video_path_tmp)
        # ФПС и суммарное количество кадров
        fps = videoCapture.get(cv2.CAP_PROP_FPS)
        frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)

        # dir_number = -1;
        # dir_name = ""

        output_video_dir = os.path.join(output_dir, video_path)
        if not os.path.exists(output_video_dir):
            os.makedirs(output_video_dir)

        for i in range(int(frames)):
            ret, frame = videoCapture.read()
            # Название кадра
            file_name = str("%d.png" % (i))
            # print(file_name.zfill(9), "/%d" % frames)

            ###################
            # Если нужно уменьшить кадр
            # frame = cv2.resize(frame, (int(frame.shape[1] / 4), int(frame.shape[0] / 4)))
            ###################

            ###################
            # Записать видео разбив его по папкам, в данном случае по 40 кадров в каждой
            # if i >= (dir_number + 1) * 40:
            #     dir_number += 1
            #     dir_name = str(dir_number).zfill(3)
            #     os.mkdir("/home/jasmine/Framing/frames/" + dir_name)
            # cv2.imwrite("/home/jasmine/Framing/frames/" + dir_name + "/" + file_name.zfill(9), frame)
            ###################

            ###################
            # Все кадры в одной папке / название папки соответствует названию видео
            cv2.imwrite(os.path.join(output_video_dir, file_name.zfill(9)), frame)
            ###################

if __name__ == '__main__':
    time_start = datetime.now()

    parser = argparse.ArgumentParser()


    # Набор видео из датасета
    parser.add_argument('--input_dir', type=str, default='./videos')
    # Кадры
    parser.add_argument('--output_dir', type=str, default='./frames')

    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir

    video_to_frames(input_dir, output_dir)


    time_end = datetime.now()
    print("Time cost = ", (time_end - time_start), "seconds")