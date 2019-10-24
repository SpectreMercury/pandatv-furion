# -*- coding: UTF-8 -*-
import hashlib
import json
import os
import urllib

import cv2
import numpy as np
from PIL import Image

hero_dict = {
    "1": "Warrior",
    "2": "Shaman",
    "3": "Rogue",
    "4": "Paladin",
    "5": "Hunter",
    "6": "Druid",
    "7": "Warlock",
    "8": "Mage",
    "9": "Priest"
}


def loadImage(url):
    img = cv2.cv2.imread(url)
    return img


def predict(path):
    dir_path = path
    try:
        image = Image.open(dir_path)
        height = image.height
        width = image.width
        port_area = (width * 0.4, height * 0.65, width * 0.6, height * 0.86)
        image = image.crop(port_area)
        image.save(dir_path)
        img = loadImage(dir_path)
        # Initiate SIFA detector
        return detect(img)
    except:
        return -1, 'notpic'


img_surf_dict = {}


def detect(dest):
    if not img_surf_dict:
        hero_arr = np.load('/home/q/system/furion/py/hs_init_hero.npy')
        init_arr = np.load('/home/q/system/furion/py/hs_init_data.npy')
        # hero_arr = np.load('hs_init_hero.npy')
        # init_arr = np.load('hs_init_data.npy')
        for hero, surf in zip(hero_arr, init_arr):
            img_surf_dict[hero] = surf

    surf_creater = cv2.cv2.xfeatures2d.SURF_create()
    dest_surf = surf_creater.detectAndCompute(dest, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv2.cv2.FlannBasedMatcher(index_params, search_params)

    img_good_dict = {}
    for img_name, img_surf in img_surf_dict.items():
        matches = flann.knnMatch(img_surf[1], dest_surf[1], k=2)
        good_dict = {}
        for m, n in matches:
            if m.distance < 0.66 * n.distance:
                good_dict[m.trainIdx] = m
        good = list(good_dict.values())
        img_good_dict[img_name] = good

    crd_dict = {}
    for img_name, img_good in sorted(img_good_dict.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
        src_pts = np.float32([img_surf_dict[img_name][0][m.queryIdx] for m in img_good]).reshape(-1, 1, 2)
        dst_pts = np.float32([dest_surf[0][m.trainIdx].pt for m in img_good]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 0.8)
        mask = mask.ravel().tolist()
        crd_dict[img_name] = mask

    max_match = sorted(crd_dict.items(), key=lambda x: x[1].count(1), reverse=True)[0]
    max_name = max_match[0]
    # max_mask = max_match[1]
    max_good = img_good_dict[max_name]
    max_num = len(max_good)

    # draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
    #                    singlePointColor=None,
    #                    matchesMask=max_mask,  # draw only inliers
    #                    flags=2)
    # img = cv2.imread(os.path.join('lol_avatar', max_name), 0)
    # img2 = cv2.drawMatches(img, img_surf_dict[max_name][0], dest, dest_surf[0], max_good, None, **draw_params)
    # cv2.imwrite(os.path.join('./lol_dest', max_name), img2)

    if max_num > 8:
        hero = hero_dict[max_name.split('-')[0]]
        return max_num, hero
    else:
        return max_num, 'unknown'


def saveImage(url):
    if not os.path.exists(os.getcwd() + '/hearthstone_hero/'):
        os.mkdir(os.getcwd() + '/hearthstone_hero/')
    file_md5 = hashlib.md5(url).hexdigest()
    file_path = os.getcwd() + '/hearthstone_hero/' + file_md5 + '.jpg'
    urllib.urlretrieve(url, file_path)
    return file_path, file_md5


def detect_img(url):
    file_path, file_md5 = saveImage(url)
    max, hero = predict(file_path)
    result = format_response(max, hero)
    result["data"]["md5"] = file_md5
    print(json.dumps(result))


def format_response(max, hero):
    global hero_map
    result = {}
    if max < 0:
        result["errno"] = 401
        result["errmsg"] = "cannot read pic"
        result["data"] = {}
    elif max <= 8:
        result["errno"] = 402
        result["errmsg"] = "detect failed"
        result["data"] = {}
    else:
        result["errno"] = 0
        result["errmsg"] = "success"
        result["data"] = {
            "heroKey": hero
        }
    return result


# url = 'http://i6.pdim.gs/84c6eeafc1bcb75e57f49e8b2f6fbee7.jpg'
# detect_img(url)
