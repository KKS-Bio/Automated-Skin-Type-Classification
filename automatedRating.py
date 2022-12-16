import numpy as np
import cv2
import glob
import os
from skimage import color
import math
import multiprocessing
from multiprocessing import Pool
from timeit import default_timer as timer
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from os import path, makedirs
import shutil
import sys

def display_image(image, name):
    window_name = name
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, image)
    cv2.waitKey()
    cv2.destroyAllWindows()

def fitzpatrick_type(ita):
    case_id=0
    case=['1','2','3','4','5','6']

    if(ita>=50):
        case_id=1
    elif(ita>=25 and ita<50):
        case_id=2
    elif(ita>=0 and ita<25):
        case_id=3
    elif(ita>=-25 and ita<0):
        case_id=4
    elif(ita>=-50 and ita<-25):
        case_id=5
    elif(ita<-50):
        case_id=6

    value = case[case_id-1]
    return value

def extractITA(k):
    ita=0
    k = [x / 255 for x in k]
    lab = color.rgb2lab([[k]])
    L = lab[0][0][0]
    a = lab[0][0][1]
    b = lab[0][0][2]
    xx = (L - 50)/b
    yy = np.arctan(xx)
    nominator = yy * 180
    denominator = math.pi
    ita1 = nominator/denominator
    ita1 = round(ita1)
    return ita1

def getMedianImageChannels(image):
    b, g, r = cv2.split(image)
    b = b[b != 0]
    g = g[g != 0]
    r = r[r != 0]
    b_median = round(np.mean(b))
    r_median = round(np.mean(r))
    g_median = round(np.mean(g))
    return r_median,g_median,b_median

def SkinThreshold(image):
        img_BGR = image
        img_YCrCb = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2YCrCb)
        blue = []
        green = []
        red = []
        height, width, channels = img_BGR.shape

        for i in range (height):
            for j in range (width):
                if((img_YCrCb.item(i, j, 0) > 70) and (136 <= img_YCrCb.item(i, j, 1) <= 173) and (77 <= img_YCrCb.item(i, j, 2) <= 127)):
                    blue.append(img_BGR[i, j].item(0))
                    green.append(img_BGR[i, j].item(1))
                    red.append(img_BGR[i, j].item(2))
                else:
                    img_BGR[i, j] = [0, 0, 0]
        #display_image(img_BGR, "final segmentation")
        return img_BGR

def skin_type(image):
    skin = SkinThreshold(image)
    median = getMedianImageChannels(skin)
    ita_score = extractITA(median)
    type_category = fitzpatrick_type(ita_score)
    return median, ita_score, type_category

def all_images(CROPPED_FACE_IMAGES_PATH):
    count=0
    #out_file_path = sys.argv[2]
    out_file_path = '/home/gabby/Desktop/rawCropped/ccRatings.txt'
    for f in glob.glob(os.path.join(CROPPED_FACE_IMAGES_PATH, "*.JPG")):
            count+=1
            o2 = open(out_file_path, 'a+')
            img = cv2.imread(f)
            dim = (512, 512)
            img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            type_category = skin_type(img)
            print(f, type_category)
            str_to_write = f.split("\\")[-1] + "," + str(type_category[0]) + "," + str(type_category[1]) + "," + str(type_category[2]) +"\n"
            o2.write(str_to_write)

if __name__ == '__main__':
    #IMAGES_PATH = sys.argv[1]
    IMAGES_PATH = '/home/gabby/Desktop/rawCropped'
    all_images(IMAGES_PATH)
