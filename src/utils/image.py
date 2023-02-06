import io
import random
from PIL import Image

def randomColor():
    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = "#"
    for i in range(6): color += colorArr[random.randint(0,14)]
    return color

def grenImageBase(width, height=None, color=None, format='PNG', mode='RGBA'):
    if height is None: height = width
    if color is None: color = randomColor()
    img = Image.new(mode, (width, height), color)
    img_byte = io.BytesIO()
    img.save(img_byte, format=format)
    return img_byte.getvalue()

def grenImagePng(*args, **kwargs):
    """
    生成指定宽高及颜色的png图片

    **Parameters:**

    * **width:** `int` -- 图片宽
    * **height:** `int` -- 图片高
    * **color:** `str` -- 图片颜色，不传时为随机颜色
    """
    return grenImageBase(*args, format='PNG', mode='RGBA', **kwargs)

def grenImageJpeg(*args, **kwargs):
    """
    生成指定宽高及颜色的jpeg图片

    **Parameters:**

    * **width:** `int` -- 图片宽
    * **height:** `int` -- 图片高
    * **color:** `str` -- 图片颜色，不传时为随机颜色
    """
    return grenImageBase(*args, format='JPEG', mode='RGB', **kwargs)

def grenImageJpg(*args, **kwargs):
    """
    生成指定宽高及颜色的jpg图片, 同`grenImageJpeg`

    **Parameters:**

    * **width:** `int` -- 图片宽
    * **height:** `int` -- 图片高
    * **color:** `str` -- 图片颜色，不传时为随机颜色
    """
    return grenImageBase(*args, format='JPEG', mode='RGB', **kwargs)

def grenImageGif(*args, **kwargs):
    """
    生成指定宽高及颜色的gif图片

    **Parameters:**

    * **width:** `int` -- 图片宽
    * **height:** `int` -- 图片高
    * **color:** `str` -- 图片颜色，不传时为随机颜色
    """
    return grenImageBase(*args, format='GIF', mode='RGB', **kwargs)
