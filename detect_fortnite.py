#!/usr/local/bin/python

from PIL import Image
from PIL import ImageEnhance
import pytesseract
import cStringIO
import urllib2
import argparse
import re
import json

SETTING_BRIGHTNESS = 0.4
SETTING_CONTRAST = 1.47
SETTING_THRESHOLD = 100

def detect_image(image):
    result = {}
    # Detect image exist
    try:
        image = cStringIO.StringIO(urllib2.urlopen(image).read())
    except Exception:
        result["errno"] = 404
        result["errmsg"] = "image does not exist"
        result["data"] = {}
        print json.dumps(result)
        return json.dumps(result)
    # Open the target image and convert to grey
    handled_image = handle_image(image)
    live_num = num_predict(pytesseract.image_to_string(handled_image, lang="eng"))
    if live_num == "" or live_num.isdigit() == False:
        live_num = "0"
    result["live"] = {
        'live-text': 'live',
        'live-num': live_num
    }
    result["errno"] = 0
    print json.dumps(result)
    return result

def handle_image(image):
  image = load_image(image)
  croped_image = crop_image(image)
  handled_iamge = brightness_image(croped_image)
  handled_image = contrast_image(handled_iamge)
  greyed_image = grey_image(handled_image)
  binaryed_image = binary_image(greyed_image)
  return binaryed_image

def load_image(path):
  return Image.open(path)

def crop_image(image):
  width = image.width
  height = image.height
  area = (width * 0.9256, height * 0.284, width *  0.95, height * 0.32)
  return image.crop(area)

def grey_image(image):
  return image.convert('L')

def binary_image(image):
  threshold = 95
  table = []
  for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
  image = image.point(table, '1')
  return image

def brightness_image(image):
  global SETTING_BRIGHTNESS
  return ImageEnhance.Brightness(image).enhance(SETTING_BRIGHTNESS)

def contrast_image(image):
  global SETTING_CONTRAST
  return ImageEnhance.Contrast(image).enhance(SETTING_CONTRAST)

def num_predict(num):
  if type(num) == unicode:
    num = num.encode('utf-8')
  if num.isdigit():
    if int(num) <= 100:
      return str(num)
    else:
      return "0"
  else:
    return filter(str.isalpha, num)