# python demosaic.py --input_dir ./out/cut_images/mishka.jpg 
import os
import numpy as np 
import cv2
import argparse
from bounding_box import BBox2D
from typing import List, Tuple


class Snippet2D:
 '''
  For recognized object on bigger source image
 '''
 def __init__(self, snippet_path: str, original_image_path: str): 
     self.snippet_path = os.path.abspath(snippet_path)
     self.original_image_path = os.path.abspath( original_image_path)
     self.name = os.path.splitext(os.path.basename(snippet_path))[0]
     print(self.name)
     image_name, x1,y1,x2,y2 = self.name.split('.')
     print(data)
     #self.bbox = 
 #def bbox_from_name(self) -> BBox2D:


    

def get_input_dir_path(input_dir : str) -> str:
    if (not input_dir):
        raise Exception("input_dir is empty")
    if (not os.path.isdir(input_dir)):
        raise Exception(f"input_dir: {input_dir} is not a directory")
    input_dir_path = os.path.abspath(input_dir)
    return input_dir_path

def get_image_paths(current_dir : str) -> List[str]:
    image_paths = []
    for root, dirs, files in os.walk(current_dir):
        for file_name in files:
            extention = os.path.splitext(file_name)[-1] 
            if extention in ['.jpg', '.png']:
                image_paths.append(os.path.join(root, file_name))
    return image_paths

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, help="path to dir with images")
    opts = parser.parse_args()
    input_dir = get_input_dir_path(opts.input_dir) 

    image_paths = get_image_paths(input_dir)
    print(image_paths)
    for image_path in image_paths:
        snippet = Snippet2D(image_path, image_path)

    

if __name__ == '__main__':
    main()

