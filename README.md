# pandatv-furion
![](https://img.shields.io/badge/building-pass-pass.svg)
![](https://img.shields.io/badge/python-v2.7-519dd9.svg)
![](https://img.shields.io/badge/opencv-4.1.2-519dd9.svg)

![](https://avatars0.githubusercontent.com/u/14814895?s=200&v=4, 'PandaTV')

A script which can extract information from live-stream images

* [Extract text information](#extract-text-information)
* [Image Recognition](#image-recognition)
---

## Extract text information

- Crop the useful area from live-stream image

- Increasing the image saturation and contrast

- Training data with jTessboxEditror and get language package

- Use [Tesseract](https://github.com/tesseract-ocr/tesseract) to extract information from image

## Image Recognition

- Use [OpenCV](https://github.com/opencv/opencv) SIFT to generate matrix of image.

- Add label to all the source image and save all the matrix into a binary file (greatly improve the matching speed)

- Compare the martrix of test image with the labeled matrix in binary file, calculate the matching rate and pick the highest.

- Iteration until the correct rate more than 85%

