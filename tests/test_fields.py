import os
import pytest

from PIL import Image

from podcast.fields import compress_image, replace_filename_suffix


@pytest.fixture
def png_image_path():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(current_dir, 'resources', 'pinscher.png')


@pytest.fixture
def png_image(png_image_path):
    """ 300x500 PNG image """

    fp = open(png_image_path, 'rb')
    yield fp
    fp.close()


@pytest.mark.parametrize('filename, expected_filename', (
    ('cu.de.cachorro.png', 'cu.de.cachorro.jpg'),
    ('file.png', 'file.jpg'),
    ('image.jpg', 'image.jpg'),
))
def test_replace_filename_suffix(filename, expected_filename):
    assert replace_filename_suffix(filename) == expected_filename


def test_compress_image(png_image, png_image_path):
    compress_image(png_image, convert_to='JPEG', quality=90, resize_to=None)

    img = Image.open(png_image_path[:-3] + 'jpg')

    assert img.width == 300  # whole size
    assert img.height == 500
    assert img.format == 'JPEG'


@pytest.mark.parametrize('resize_to, expected_size', (
    ((150, 250), (150, 250)),
    ((0, 50), (30, 50)),
    ((15, 0), (15, 25)),
))
def test_compress_image_simple_resize(png_image, png_image_path, resize_to, expected_size):
    compress_image(png_image, convert_to='JPEG', quality=90, resize_to=resize_to)

    img_path = png_image_path[:-3] + 'jpg'
    img = Image.open(img_path)

    assert img.size == expected_size
    assert img.format == 'JPEG'

    os.remove(img_path)
