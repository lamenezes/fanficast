import re

from django.db import models

_filetype_regex = re.compile(r'(.*)\.(.*)+$')


def replace_filename_suffix(filename):
    return _filetype_regex.sub(r'\1.jpg', filename)


def compress_image(fp, convert_to, resize_to, quality):
    """
    compress an image given the passed arguments. keeps the source image and creates a new one.
    """

    from PIL import Image

    image = Image.open(fp)

    if image.mode != 'RGB':
        image = image.convert('RGB')

    if resize_to:
        new_width, new_height = resize_to

        if new_width == 0:
            new_width = image.width

        if new_height == 0:
            new_height = image.height

        image.thumbnail((new_width, new_height), Image.ANTIALIAS)

    try:
        filename = fp.path
    except AttributeError:
        filename = fp.name

    filename = replace_filename_suffix(filename)
    image.save(filename, format='JPEG', quality=quality)
    return image


class CompressedImageField(models.ImageField):
    """
    A field that automatically compress uploaded images
    """

    convert_to = 'JPEG'
    resize_to = None
    image_quality = 80

    def __init__(self, *args, **kwargs):
        self.convert_to = kwargs.pop('convert_to', self.convert_to)
        self.resize_to = kwargs.pop('resize_to', self.resize_to)
        self.image_quality = kwargs.pop('image_quality', self.image_quality)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        file = super().pre_save(model_instance, add)

        new_filename = replace_filename_suffix(file.name)
        image_field = getattr(model_instance, self.name)
        file.name = image_field.file.name = new_filename

        compress_image(
            file,
            resize_to=self.resize_to,
            convert_to=self.convert_to,
            quality=self.image_quality,
        )
        return file

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        if self.convert_to != 'JPEG':
            kwargs['convert_to'] = self.convert_to

        if self.resize_to:
            kwargs['resize_to'] = self.resize_to

        if self.image_quality != 80:
            kwargs['image_quality'] = self.image_quality

        return name, path, args, kwargs
