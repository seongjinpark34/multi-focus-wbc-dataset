import cv2
import numpy as np

import argparse
from process import DataWangler
import glob
import os

def get_best_focus_laplacian(image_list):
    fm_list = []
    for img in image_list:
        
        fm_list.append(get_laplacian_fm(cv2.imread(img)))

    return np.array(fm_list).argmax()

def get_laplacian_fm(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(gray_image, cv2.CV_64F)
    fm = lap.var()
    return fm


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_dir", type=str, help="test directory")
    parser.add_argument("--cell", type=int, help="cell index to get best focused image" )
    args = parser.parse_args()
    img_list = glob.glob(os.path.join(args.test_dir, f"{args.cell}_*.jpg"))
    # print(f"{target_folder} is created properly.")
    if len(img_list) == 0:
        raise Exception("No image is in the specified directory.")
    focus = get_best_focus_laplacian(img_list)
    print(f"The best focus index for image {args.cell} is {focus}, which is {args.cell}_{focus}.jpg under the folder {args.test_dir}.")
