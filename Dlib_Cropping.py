import dlib
import os
import cv2
import time
import numpy as np

def dlib_module(name,face_file_path,save_directory):
    img = dlib.load_rgb_image(face_file_path)
    desiredDim = (200, 240)
    origH = img.shape[0]
    origW = img.shape[1]
    if (origW,origH)!=desiredDim:
        img = cv2.resize(img, desiredDim, interpolation=cv2.INTER_AREA)
    detector = dlib.get_frontal_face_detector()
    dets = detector(img, 1)
    if (len(dets) < 1):
        print("Error cropping Image: " + name+"\n")
        return
    for i, d in enumerate(dets):
        win = dlib.image_window()
        win.clear_overlay()
        win.set_image(img)
        win.add_overlay(dets)
        crop_img = img[d.top():d.bottom(), d.left():d.right()]
        if np.size(crop_img)==0:
            print("Error cropping Image: " + name+"\n")
            return
        cropped_img = cv2.resize(crop_img, (224, 224))
        color_crop_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
        os.chdir(save_directory)
        cv2.imwrite(name, color_crop_img)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Crop face images.')
    parser.add_argument('-predictor', '-p', help='Path to predictor .dat file (e.g. shape_predictor_68_face_landmarks.dat).')
    parser.add_argument('-images', '-i', help='Path to folder containing face images.')
    parser.add_argument('-savedir', '-sd', help='Path to folder to save cropped images in.')
    args = parser.parse_args()

    inputPath = args.images
    numImgs = len(os.listdir(inputPath))
    predictor_path = args.predictor
    sp = dlib.shape_predictor(predictor_path)

    for basefilename in os.listdir(inputPath):
        print("Running file: %s"%basefilename)
        face_file_path = os.path.join(inputPath, basefilename)
        dlib_module(basefilename,face_file_path,args.savedir)
