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
        print("Обработка", video_path)

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
            # Заносим кадры в буффер для дальнейшей обработки
            if (len(buf) == 0):
                buf = np.expand_dims(frame, axis=0)
            else:
                buf = np.concatenate((buf, np.expand_dims(frame, axis=0)), axis=0)



                # print("----------------------------------------------------------------")
                # print("kendall_coefficient =", kendall_coefficient(buf[i - 1], buf[i]))
                # print("cross_correlation_coefficient =", cross_correlation_coefficient(buf[i - 1], buf[i]))
                # print("tanimoto_coefficient", tanimoto_coefficient(buf[i - 1], buf[i]))


                # Вычисляем корреляцию
                coef_pair_frame = np.array([kendall_coefficient(buf[i - 1], buf[i]), i - 1, i])

                # Записываем корреляцию для дальнейшего анализа
                if (len(coef_pair_frame_array) == 0):
                    coef_pair_frame_array = np.expand_dims(coef_pair_frame, axis=0)
                else:
                    coef_pair_frame_array = np.concatenate((coef_pair_frame_array, np.expand_dims(coef_pair_frame, axis=0)), axis=0)

        # Нужно найти пары кадров с подходящей корреляцией
        print(coef_pair_frame_array)
        # print(coef_pair_frame_array[:, 0])
        # print("Среднее ->", coef_pair_frame_array[:, 0].mean())

        # К какой корреляции должны стремиться выбираемые кадры
        need_coef = 0.985 # Нужно указыват ьв стартовых параметрах

        # Сколько пар кадров берем из одного видео
        need_count = 5
        # На столько частей нам нужно поделить видео
        # и выбрать в каждой части пару наиболее близкую к need_coef

        # Проходим по участкам одинаковой длины
        for i in range(need_count):
            # Вычисляем длинну участка
            frames_range_a = len(coef_pair_frame_array) // need_count + 1
            frames_range_b = frames_range_a
            # print("frames_range ->", frames_range_b)
            # Проверяем что не выходим за границы массива
            # print("IF", i * frames_range_b + frames_range_b - 1, "----", len(coef_pair_frame_array) - 1)
            if i * frames_range_b + frames_range_b - 1 > len(coef_pair_frame_array) - 1:
                # Вычисляем новую длину
                frames_range_b += len(coef_pair_frame_array) - i * frames_range_b - frames_range_b
                # print("NEW frames_range ->", frames_range_b)

            print(f"({i * frames_range_a}, { i * frames_range_a + frames_range_b - 1 })")

            # Нужный срез
            frames_coef = coef_pair_frame_array[i * frames_range_a : i * frames_range_a + frames_range_b]

            # Находим запись с корреляцией, абсолютное значение разности которого, с нужным коэффициентом - минимально
            condition = np.abs(frames_coef[:, 0] - need_coef)
            frames_coef = frames_coef[condition == np.min(condition)]

            # Нужно учесть что в срезе может не быть ни одной пары


            # Сохраняем выделенную пару в соответствующей папке
            direction = os.path.join(output_dir, video_path, str(i).zfill(3) + " coef:" + str(frames_coef[0][0])[:6])
            if not os.path.exists(direction):
                os.makedirs(direction)

            # Сохраняем пару кадров
            print(os.path.join(direction, str(int(frames_coef[0][1])).zfill(5)))
            print(os.path.join(direction, str(int(frames_coef[0][2])).zfill(5)))
            cv2.imwrite(os.path.join(direction, str("%s.png" % str(int(frames_coef[0][1])).zfill(5))), buf[int(frames_coef[0][1])])
            cv2.imwrite(os.path.join(direction, str("%s.png" % str(int(frames_coef[0][2])).zfill(5))), buf[int(frames_coef[0][2])])

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