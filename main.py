from os import listdir
import random
from moviepy.editor import concatenate_videoclips, vfx, AudioFileClip, afx, ImageClip, CompositeAudioClip, \
    CompositeVideoClip
from PIL import Image
import cv2
import shutil
import time


input_path_photo = 'input_path_for_photo'
input_path_audio = 'input_path_for_audio'
list_dir_with_photo = listdir(input_path_photo)
list_dir_with_audio = listdir(input_path_audio)
list_dir_with_background = listdir('background')
list_dir_with_logo = listdir('logo')


def check_name_files():
    extentions_list = ['jpg', 'jpeg', 'png']
    eror_extention_list = []
    for dir in list_dir_with_photo:
        if len(list_dir_with_photo)==0:
            return 0
        list_photo = listdir(f'{input_path_photo}/{dir}')
        path = f'{input_path_photo}/{dir}/'
        for i in list_photo:
            extention_file = i.split(".")[1]
            if extention_file not in extentions_list:
                i = path + i
                eror_extention_list.append(i)
    if len(eror_extention_list) != 0:
        print(f'''
У этих файлов неподходящее расширение{eror_extention_list}
Список расширений который поддерживает программа: jpg, jpeg, png.
        ''')
        return False
    else:
        return True


def watermark_photo(file):
    base_image = Image.open(file)
    watermark = Image.open("logo/logo.png")
    size = watermark.size
    w = size[0]
    h = size[1]
    first = round((1080 - w) / 2)
    final = base_image.paste(watermark, (first, 20))
    base_image.save(file)
    # add watermark to your image
    return final




def convert_photo_to_video(mode = None, position = None):
    """
    :param mode: имеет значения True (тогда в средние видео подставляется лого из папки logo) или False
    :return:
    """
    try:
        if len(list_dir_with_photo) == 0:
            print('во входно папке для фото пусто, программа сейчас закроется')
            time.sleep(5)
            return 0
        if check_name_files() == True:
            for dir in list_dir_with_photo:
                if len(list_dir_with_audio)==0:
                    print('в папке c audio пусто')
                    time.sleep(5)
                    return
                if len(list_dir_with_logo)==0:
                    print('в папке logo пусто')
                    time.sleep(5)
                    return
                if len(list_dir_with_background)==0:
                    print('в папке background пусто')
                    time.sleep(5)
                    return
                list_photo = listdir(f'{input_path_photo}/{dir}')
                path = f'{input_path_photo}/{dir}/'
                img = []
                for i in list_photo:
                    i = path + i
                    img.append(i)

                # count_photos_in_middle = len(list_photo) - 2
                one_duration = random.randint(3, 7)
                end_duration = random.randint(4, 8)
                a = 2
                if 'one.*' not in list_photo:
                    one_duration = 0
                    a = a - 1
                if 'end.*' not in list_photo:
                    end_duration = 0
                    a = a - 1
                count_photos_in_middle = len(list_photo) - a
                middle_duration = (59 - one_duration - end_duration) / count_photos_in_middle
                movies_list = []
                for photo in img:
                    image = Image.open(photo)
                    size = image.size
                    k = 1080 / size[0]
                    w = round(k * size[0])
                    h = round(k * size[1])
                    vstavka = round((1920 - h) / 2)
                    new_image = image.resize((w, h))
                    new_image.save(photo)
                    name_photo = photo.replace(f'{path}', '').split(".")[0]
                    black = Image.open('background/background.jpg')
                    top = Image.open(photo)
                    black.paste(top, (0, vstavka))
                    black.save(photo)
                    if name_photo == 'one':
                        clip_one = ImageClip(photo).set_duration(one_duration).fx(vfx.fadein, random.randint(0, 2)).fx(vfx.fadeout, random.randint(0, 2))
                        movies_list.insert(0, clip_one)
                        continue
                    if name_photo == 'end':
                        clip_end = ImageClip(photo).set_duration(end_duration).fx(vfx.fadein, random.randint(0, 2)).fx(vfx.fadeout, random.randint(0, 2))
                        movies_list.append(clip_end)
                        continue
                    if name_photo not in ['one', 'end']:
                        if mode == 'None':
                            clip_middle = ImageClip(photo).set_duration(middle_duration).fx(vfx.fadein, random.randint(0, 2)).fx(vfx.fadeout, random.randint(0, 2))
                            movies_list.append(clip_middle)
                            continue
                        if mode == 'True':
                            image = cv2.imread(photo)
                            font = cv2.FONT_HERSHEY_COMPLEX
                            if position == 'top':
                                cv2.putText(image, text, (17, 180), fontScale=2, fontFace=font,
                                        color=(255, 255, 255), thickness=3)
                                cv2.imwrite(photo, image)
                                clip_middle = ImageClip(photo).set_duration(middle_duration).fx(vfx.fadein, random.randint(0, 2)).fx(vfx.fadeout, random.randint(0, 2))
                                movies_list.append(clip_middle)
                                continue
                            if position == 'down':
                                cv2.putText(image, text, (17, 1800), fontScale=2, fontFace=font,
                                            color=(255, 255, 255), thickness=3)
                                cv2.imwrite(photo, image)
                                clip_middle = ImageClip(photo).set_duration(middle_duration).fx(vfx.fadein, random.randint(0, 2)).fx(vfx.fadeout, random.randint(0, 2))
                                movies_list.append(clip_middle)
                                continue
                        if mode == 'Logo':
                            watermark_photo(photo)
                            clip_middle = ImageClip(photo).set_duration(middle_duration).fx(vfx.fadein, random.randint(0, 2)).fx(vfx.fadeout, random.randint(0, 2))
                            movies_list.append(clip_middle)
                            continue
                        else:
                            continue
                    else:
                        continue

                audio_list = listdir('input_path_for_audio')
                audio_num = random.randint(0, len(audio_list)-1)
                audio = AudioFileClip(f'{input_path_audio}/{audio_list[audio_num]}').fx(afx.volumex, 0.5)
                video_clip = concatenate_videoclips(movies_list, method='compose')
                video_clip.audio = CompositeAudioClip([audio])
                video_clip.write_videofile(f'finish_videos/video_out-2{dir}.mp4', fps=30, remove_temp=True, codec='libx264')
                shutil.rmtree(path)

        else:
            print('Что то не так с фото, проверьте их наличие или расширение')
            time.sleep(4)

    except Exception as e:
        print(e)


print("""
Ленивый монтаж 2.0
Программа поддерживает 3 режима работы
True - С надписью на видео "ссылка на товар в описании"
None - Без надписи и вставки фото
Logo - Вставка изображения типа watermark
""")
mode = input('Введите режим работы (True, None или Logo):')
mode = mode

if mode in ['True', 'true']:
    position = input('Выберите положение надписи (top или down):')
    if position == 'down':
        text = 'ссылка на товар в описании'
        convert_photo_to_video(mode='True', position='down')
    if position == 'top':
        text = 'ссылка на товар в описании'
        convert_photo_to_video(mode='True', position='top')
if mode in ['Logo', 'logo']:
    print('Логотип будет расположен сверху')
    convert_photo_to_video(mode='Logo', position='top')
if mode in ['None', 'none']:
    convert_photo_to_video(mode='None')

