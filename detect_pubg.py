#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

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

def detect_image(image, cate):
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
    image = Image.open(image)
    live_image = handle_image(image, cate)
    #Get the Result
    live_num = num_predict(pytesseract.image_to_string(live_image, lang="pubg"))
    #kill_num = num_predict(pytesseract.image_to_string(kill_image, lang="pubg"))
    #Get the type
    #kill_text = type_predic(pytesseract.image_to_string(live_image, lang="chi_sim"))

    #When PUBG is a match live
    # if kill_text == 'unknown':
    #     kill_num = ''
    result["live"] = {
        'live-text': 'live',
        'live-num': live_num
    }
    result["errno"] = 0
    print json.dumps(result)
    return result

def handle_image(img, cate):
    height = img.height
    width = img.width
    if cate == "pubg":
      live_area = (width * 0.928125, height / 36, width * 0.94921875, height * 0.064)
    elif cate == "cjzc":
      live_area = (width * 0.085, height * 0.0055, width * 0.0989, height * 0.03055)
    img = img.crop(live_area)
    img = image_contrast(img)
    img = image_binary(img)
    return img


def image_contrast(img):
    global SETTING_CONTRAST
    global SETTING_BRIGHTNESS
    # factor = (259 * (SETTING_CONTRAST + 255)) / (255 * (259 - SETTING_CONTRAST))
    # def contrast(c):
    #     return 128 + factor * (SETTING_CONTRAST - 128)
    image = ImageEnhance.Contrast(img).enhance(SETTING_CONTRAST)
    #a = img.point(contrast)
    image = ImageEnhance.Brightness(image).enhance(SETTING_BRIGHTNESS)
    return image

def image_binary(image):
    global SETTING_THRESHOLD
    threshold = SETTING_THRESHOLD
    image = image.convert('L')
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')
    return image


def num_predict(content):
    if content.isdigit():
        if int(content) > 1000 :
            content = 0
        elif int(content) > 100 :
            content = str(content)[1:3]
    else :
        content = 0
    content = str(content)
    return content

