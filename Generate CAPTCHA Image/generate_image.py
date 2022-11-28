from captcha.image import ImageCaptcha
import string
import random

image = ImageCaptcha(width=160, height=60,
                    fonts=None, font_sizes=None)
code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
image.write(code, 'captcha.png')