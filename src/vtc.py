import datetime
import os
import re

import yt_dlp
from yt_dlp.utils import download_range_func

from aiogram.filters import CommandObject
from aiogram.types import Message, FSInputFile

from moviepy.editor import VideoFileClip
from moviepy.video.fx import margin

youtube_regex = r"^(((https:\/\/)?w{3}\.youtube\.com)|(youtube\.com))(\/watch\?v=.*$)"
time_format_regex = r"^([0-5][0-9]:){2}[0-5][0-9]$"
duration_regex = r"^(([0-9])||([1-5][0-9])||60)$"

youtube_pattern = re.compile(youtube_regex)
time_format_pattern = re.compile(time_format_regex)
duration_pattern = re.compile(duration_regex)


def download(link, name='%(title)s', start_time="00:00:00", duration=60):
    temp = datetime.datetime.strptime(start_time, "%H:%M:%S")
    start = (temp.hour * 60 * 60) + temp.minute * 60 + temp.second
    end = start + duration
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best', #берем самое лучшее качество видео и фото
        'outtmpl': '{}.%(ext)s'.format(name), #наше выбраное имя, если его не было, то стандартное - название видео на самом сайте
        'download_ranges': download_range_func(None, [(start, end)]),
        'force_keyframes_at_cuts': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=True)
        downloaded_file_path = ydl.prepare_filename(info_dict)
    print(f"Видео {downloaded_file_path} успешно загружено!")
    return downloaded_file_path


async def process_and_send_video(message: Message, video_file_path: str, flag_crop:bool = False) -> None:
    # Путь к временно обработанному файлу
    processed_video_path = "processed_video.mp4"

    try:
        # Открытие исходного видеофайла
        print(video_file_path)
        video_clip = VideoFileClip(video_file_path)
        duration = video_clip.duration
        width, height = video_clip.size

        if not flag_crop and width != height:
            # Дополнение видео до квадратного
            size = max(width, height)
            video_clip = margin.margin(
                video_clip, top=(size - height) // 2,
                bottom=(size - height) // 2,
                left=(size - width) // 2,
                right=(size - width) // 2, color=(0, 0, 0)
            )

        if flag_crop and width != height:
            min_size = min(width, height)
            center_x, center_y = width // 2, height // 2
            temp = min_size // 2
            # Обрезка видео до квадратного
            video_clip = video_clip.crop(
                x1=center_x - temp,
                y1=center_y - temp,
                x2=center_x + temp,
                y2=center_y + temp
            )

        video_resized = video_clip.resize((400, 400))


        # Обрезка видео до одной минуты
        if duration > 60:
            video_resized = video_resized.subclip(0, 60)
        # Сохранение обработанного видео
        video_resized.write_videofile(processed_video_path, codec="libx264", bitrate="1000k")
        # Отправка видео как видеосообщение
        video = FSInputFile(processed_video_path)
        await message.answer_video_note(video)

    except Exception as e:
        print(type(e))
        print(e)
        await message.answer(f"Oops something went wrong")

    finally:
        # Очистка временного файла
        if os.path.exists(processed_video_path):
            os.remove(processed_video_path)
        os.remove(video_file_path)

async def process_vtc_command(message: Message, command: CommandObject, flag_corp: bool = False):
    args_ = list(filter(None, command.args.split(" ")))

    link = ""
    start_time = "00:00:00"
    duration = "60"

    if len(args_) < 0 or len(args_) > 3:
        return await message.answer("Incorrect command format")
    if not youtube_pattern.match(args_[0]):
        return await message.answer("The link is not valid")
    else:
        link = args_[0]
    if len(args_) == 2:
        if time_format_pattern.match(args_[1]):
            start_time = args_[1]
        elif duration_pattern.match(args_[1]):
            duration = args_[1]
        else:
            return await message.answer("Error over time")
    if len(args_) == 3:
        if not time_format_pattern.match(args_[1]):
            return await message.answer("Wrong time format")
        elif not duration_pattern.match(args_[2]):
            return await message.answer("Wrong duration")
        else:
            start_time = args_[1]
            duration = args_[2]

    print(link)
    print(start_time)
    print(int(duration))
    await message.answer("Request processing...")
    video_name = f"video_{datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}"
    video_path = download(link, video_name, start_time, int(duration))
    await process_and_send_video(message, video_path, flag_corp)