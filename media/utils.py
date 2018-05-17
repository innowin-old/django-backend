import os
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from moviepy.editor import *
import sys


def compress_video(file):
    clip = VideoFileClip(file)
    clip = clip.resize(width=854, height=480)
    clip = clip.volumex(0.8)
    compressed_file = clip.write_videofile(get_file_name(file) + "_edited.mp4", codec='libx264')
    return compressed_file


def compress_image(image, usage):
    # Opening the uploaded image
    im = Image.open(image)
    output = BytesIO()
    if usage == 'profile_media' or usage == 'organization_logo':
        # Resize/modify the image
        # im = im.resize((100, 100))
        # after modifications, save it to the output
        im.save(output, format='JPEG', quality=50)
    elif usage == 'profile_banner' or usage == 'organization_banner':
        # after modifications, save it to the output
        im.save(output, format='JPEG', quality=80)
    else:
        # after modifications, save it to the output
        im.save(output, format='JPEG', quality=100)
    output.seek(0)
    return InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)


def get_file_name(file):
    return os.path.basename(file.name)