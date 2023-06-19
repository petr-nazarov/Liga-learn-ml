import os
import cv2
import numpy as np
import random
from typing import List, Tuple
from enum import Enum

class Mode(Enum):
    color_black = 1 
    cut_images = 2
current_dir = os.getcwd()


def get_image_paths(current_dir : str) -> List[str]:
    image_paths = []
    for root, dirs, files in os.walk(current_dir):
        for file_name in files:
            extention = os.path.splitext(file_name)[-1] 
            if extention in ['.jpg', '.png']:
                image_paths.append(os.path.join(root, file_name))
    return image_paths

def calculate_area_coordinates(image : np.ndarray, divider_h : int, divider_w : int, sub_area_h: int, sub_area_w:int,  row_index : int, col_index : int) -> Tuple[int, int, int, int, int, int, int, int]:
                y_top = row_index * sub_area_h 
                y_bottom = (row_index + 1) * sub_area_h
                x_left = col_index * sub_area_w
                x_right = (col_index + 1) * sub_area_w
                center_y = int(np.round((y_top + y_bottom) / 2))
                center_x = int(np.round((x_left + x_right) / 2))
                center_radius_x= sub_area_w // 10
                center_radius_y= sub_area_w // 10

                return y_top, y_bottom, x_left, x_right, center_y, center_x, center_radius_x, center_radius_y
def calculate_image_division(image : np.ndarray, h: int, w: int, divider_h : int = 10, divider_w : int = 6) -> Tuple[int, int]:
    sub_area_h = int(np.round(h / divider_h))
    sub_area_w = int(np.round(w / divider_w))
    return sub_area_h, sub_area_w

def create_cut_subimages(image_path: str, image_name: str, out_path: str, divider_h : int = 10, divider_w : int = 6, ):
    image = cv2.imread(image_path, 1)
    name_without_extention, extention = os.path.splitext(image_name)
    h, w, c = image.shape
    sub_area_h, sub_area_w = calculate_image_division(image, h, w, divider_h, divider_w)
    for row_index in range(divider_h):
        for col_index in range(divider_w):
                y_top, y_bottom, x_left, x_right, center_y, center_x, center_radius_x, center_radius_y = calculate_area_coordinates(image, divider_h, divider_w, sub_area_h, sub_area_w, row_index, col_index)
                sub_image = image[
                     y_top : y_bottom,
                     x_left : x_right,
                ]
                out_name = f"{name_without_extention}.{x_left}.{y_top}.{x_right}.{y_bottom}{extention}"
                print(f"Saving {out_name}")
                cv2.imwrite(os.path.join(out_path, out_name), sub_image)

def get_shahmatka_from_image(image_path : str , divider_h : int = 10, divider_w : int = 6) -> np.ndarray:
    is_color_iamge = 1
    image = cv2.imread(image_path, is_color_iamge)
    if is_color_iamge:
        h, w, c = image.shape
    else:
        h, w = image.shape
    sub_area_h, sub_area_w = calculate_image_division(image, h, w, divider_h, divider_w)
    row_starts_with_black = True 
    for row_index in range(divider_h):
        if row_starts_with_black:
            black_index = 0
        else:
            black_index = 1
        for col_index in range(divider_w):
                y_top, y_bottom, x_left, x_right, center_y, center_x, center_radius_x, center_radius_y = calculate_area_coordinates(image, divider_h, divider_w, sub_area_h, sub_area_w, row_index, col_index)
                if black_index % 2 == 0:
                    image[
                        y_top : y_bottom,
                        x_left : x_right,
                    ] *= 0
                image[
                    center_y - center_radius_y : center_y + center_radius_y,
                    center_x - center_radius_x: center_x + center_radius_x,
                ] = (0,0,255)
                black_index += 1
                image = cv2.circle(image, (center_x, center_y), center_radius_x // 2, (160, 10, 45), -1)
        row_starts_with_black = not row_starts_with_black
    return image

def main(mode : Mode = Mode.color_black):
    image_paths = get_image_paths(os.path.join(current_dir, "test_data"))
    for image_path in image_paths:
        #divider_h = random.randint(2, 10)
        #divider_w = random.randint(2, 10)
        divider_h = 10 
        divider_w = 10
        image_name = os.path.basename(image_path)
        print(f"Processing {image_name}")
        if mode == Mode.color_black:
            new_image = get_shahmatka_from_image(image_path, divider_h, divider_w )
            out_dir = os.path.join(current_dir, "out")
            out_path = os.path.join(out_dir, 'shhmatka_' + image_name)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir, exist_ok=True)
            cv2.imwrite(out_path, new_image)
            print(f"Saved to {out_path}")
        elif mode == Mode.cut_images:
            out_dir = os.path.join(current_dir, "out", "cut_images", image_name)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir, exist_ok=True)
            create_cut_subimages(image_path, image_name, out_dir, divider_h, divider_w )
if __name__ == "__main__":
    main(Mode.cut_images)
