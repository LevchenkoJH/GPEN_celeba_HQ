import cv2
import os
from datetime import datetime
import argparse

import numpy as np
from tqdm import tqdm

from сoefficients import tanimoto_coefficient
from сoefficients import cross_correlation_coefficient
from сoefficients import kendall_coefficient



def video_to_frames(input_dir, output_dir):
    dirs = sorted(os.listdir(input_dir))
    print(dirs)

    for video_path in tqdm(dirs):

        # Расшариваем видео в буфере (frames)
        video_path_tmp = os.path.join(input_dir, video_path)
        videoCapture = cv2.VideoCapture()
        videoCapture.open(video_path_tmp)
        frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)

        # output_video_dir = os.path.join(output_dir, video_path)
        # if not os.path.exists(output_video_dir):
        #     os.makedirs(output_video_dir)


        # Буфер изображений
        # Из него выбираем кадры, которые будут сохранены для датасета
        buf = np.array([])

        # Структура
        # [коэффициент корреляции, индекс первого изображения, индекс второго изображения]
        coef_pair_frame_array = np.array([])
        for i in range(int(frames)):
            ret, frame = videoCapture.read()
            # Заносим кадры в буффер
            if (len(buf) == 0):
                buf = np.expand_dims(frame, axis=0)
            else:
                buf = np.concatenate((buf, np.expand_dims(frame, axis=0)), axis=0)



                # print("----------------------------------------------------------------")
                # print(i - 1, i)
                # print(buf[i - 1].shape, buf[i].shape)
                # print("kendall_coefficient =", kendall_coefficient(buf[i - 1], buf[i]))
                # print("cross_correlation_coefficient =", cross_correlation_coefficient(buf[i - 1], buf[i]))
                # print("tanimoto_coefficient", tanimoto_coefficient(buf[i - 1], buf[i]))

                coef_pair_frame = np.array([kendall_coefficient(buf[i - 1], buf[i]), i - 1, i])
                # coef_pair_frame = np.expand_dims(coef_pair_frame, axis=0)

                if (len(coef_pair_frame_array) == 0):
                    coef_pair_frame_array = np.expand_dims(coef_pair_frame, axis=0)
                else:
                    coef_pair_frame_array = np.concatenate((coef_pair_frame_array, np.expand_dims(coef_pair_frame, axis=0)), axis=0)


                # print(coef_pair_frame_array.shape)
        print(coef_pair_frame_array)

            # print(i + 1, "->", buf.shape)
    #
    #
    #     # print("buf.shape", buf.shape)



        # for i in range(int(frames)):
        #     ret, frame = videoCapture.read()
        #     # Название кадра
        #     file_name = str("%d.png" % (i))
        #
        #     ###################
        #     # Если нужно уменьшить кадр
        #     # frame = cv2.resize(frame, (int(frame.shape[1] / 4), int(frame.shape[0] / 4)))
        #     ###################
        #
        #     ###################
        #     # Записать видео разбив его по папкам, в данном случае по 40 кадров в каждой
        #     # if i >= (dir_number + 1) * 40:
        #     #     dir_number += 1
        #     #     dir_name = str(dir_number).zfill(3)
        #     #     os.mkdir("/home/jasmine/Framing/frames/" + dir_name)
        #     # cv2.imwrite("/home/jasmine/Framing/frames/" + dir_name + "/" + file_name.zfill(9), frame)
        #     ###################
        #
        #     ###################
        #     # Все кадры в одной папке / название папки соответствует названию видео
        #     cv2.imwrite(os.path.join(output_video_dir, file_name.zfill(9)), frame)
        #     ###################

if __name__ == '__main__':
    time_start = datetime.now()
    parser = argparse.ArgumentParser()
    # Набор видео из датасета
    parser.add_argument('--input_dir', type=str, default='./videos')
    # Подготовленный датасет
    parser.add_argument('--output_dir', type=str, default='./frames')
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir

    video_to_frames(input_dir, output_dir)
    time_end = datetime.now()
    print("Time cost = ", (time_end - time_start), "seconds")