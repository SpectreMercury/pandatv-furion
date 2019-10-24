from PIL import Image
import hashlib
import urllib
import urllib2
# import 

# def detect_img(url):
  # try:
  #   image = cStringIO.StringIO(urllib2.urlopen(url).read())
  # except Exception:
  #   print 'Unknown'

def save_ori(url):
  this_url = url
  this_name = hashlib.md5(this_url).hexdigest()
  this_path = './lol_ori/' + this_name + '.jpg'
  urllib.urlretrieve(this_url, this_path)
  return this_path

def save_crop(path):
  image = Image.open(path)
  width = image.width
  height = image.height
  port_area = (width * 0.325, height * 0.916, width * 0.362, height * 0.963)
  image = image.crop(port_area)