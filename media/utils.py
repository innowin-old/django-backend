import os
from moviepy.editor import *


def compress_video(file):
    clip = VideoFileClip(file)
    print('salam')
    clip = clip.resize(width=854, height=480)
    print('salam1')
    # Reduce the audio volume (volume x 0.8)
    clip = clip.volumex(0.8)
    print('salam2')
    compressed_file = clip.write_videofile(get_file_name(file) + "_edited.mp4", codec='libx264')
    print('salam akhar')
    return compressed_file


def get_file_name(file):
    return os.path.basename(file.name)