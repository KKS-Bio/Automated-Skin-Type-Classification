import dlib
import os
import cv2
import time
import numpy as np

def dlib_module(name,face_file_path):
    img = dlib.load_rgb_image(face_file_path)
    desiredDim = (200, 240)
    origH = img.shape[0]
    origW = img.shape[1]
    if (origW,origH)!=desiredDim:
        img = cv2.resize(img, desiredDim, interpolation=cv2.INTER_AREA)
    detector = dlib.get_frontal_face_detector()
    dets = detector(img, 1)
    if (len(dets) < 1):
        noFaceList.write((name + "\n"))
        return
    for i, d in enumerate(dets):
        win = dlib.image_window()
        win.clear_overlay()
        win.set_image(img)
        win.add_overlay(dets)
        crop_img = img[d.top():d.bottom(), d.left():d.right()]
        if np.size(crop_img)==0:
            errorImgList.write((name+"\n"))
            return
        cropped_img = cv2.resize(crop_img, (224, 224))
        color_crop_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
        os.chdir('/home/gabby/Desktop/rawCropped') # DIRECTORY TO save cropped images in
        cv2.imwrite(name, color_crop_img)

if __name__ == '__main__':

    inputPath = '/home/gabby/Downloads/Book'
    numImgs = len(os.listdir(inputPath))
    donesofar = 0
    predictor_path = "/home/gabby/Downloads/shape_predictor_68_face_landmarks.dat"
    sp = dlib.shape_predictor(predictor_path)
    start_time = time.time()

    for basefilename in os.listdir(inputPath):
        print("Running file: %s"%basefilename)
        face_file_path = os.path.join(inputPath, basefilename)
        dlib_module(basefilename,face_file_path)
        current_time = time.time()
        elapsed = current_time - start_time
        donesofar+=1
        estRem = (elapsed/donesofar)*(numImgs-donesofar)
        print("%d/%d | %fs passed | est. %fs remaining" %(donesofar,numImgs,elapsed,estRem))

    noFaceList.close()
