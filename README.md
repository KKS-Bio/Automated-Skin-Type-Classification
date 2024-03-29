# Automated-Skin-Type-Classification
Automated analysis of skin tone from face images

Pre-processing requirements:
1. Before color correction, each image to be processed must have the background removed as well -- I used the background removal tool available at https://github.com/OPHoperHPO/image-background-remove-tool. The matlab code requires both the original image and the background-removed version.

Required files:
1. Download the dlib "shape_predictor_68_face_landmarks.dat" file.

STEPS:
1. For all images to be color-corrected, use a background removal tool (like the one mentioned above) to create a background-removed version.
2. Generate a list of filenames for all images to be processed.
3. The MATLAB code requires: (1) folder of full original images with .JPG ext, (2) folder of background-removed images with .PNG ext, (3) list of image filenames - must be the same across both sets of images (with only the extension different).
4. Once images are color-corrected, use the Dlib_Cropping.py to crop the images.
5. The color-corrected and cropped images will be used as input for automatedRating.py.

Please cite the paper below if you use the automated skin type classification script or steps here.

# [Analysis of Manual and Automated Skin Tone Assignments](https://openaccess.thecvf.com/content/WACV2022W/DVPB/papers/Krishnapriya_Analysis_of_Manual_and_Automated_Skin_Tone_Assignments_WACVW_2022_paper.pdf)
``` r
@inproceedings{krishnapriya2022analysis,
  title={Analysis of Manual and Automated Skin Tone Assignments},
  author={Krishnapriya, KS and Pangelinan, Gabriella and King, Michael C and Bowyer, Kevin W},
  booktitle={Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision},
  pages={429--438},
  year={2022}
}
```
